"""Busca de cartões vencidos e submissão de revisões (aplica o SM-2)."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import or_, select

from app.deps import DbSession, Reader, Writer
from app.models import Card, ReviewLog, ReviewState, User
from app.schemas import DueCardOut, DueCardsOut, ReviewCreate, ReviewResult
from app.scoring import points_for_review
from app.srs import Sm2State, initial_state, review as apply_sm2
from app.stats import reviews_today, today_in_study_tz

# Teto de segurança para "revisar tudo" — evita devolver centenas de cartões.
MAX_DUE_CARDS = 100

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


def _visible_to(user: User):
    return or_(Card.owner_id.is_(None), Card.owner_id == user.id)


@router.get("/due", response_model=DueCardsOut)
def list_due_cards(
    db: DbSession,
    current_user: Reader,
    include_all: bool = False,
):
    """Cartões vencidos (ou novos), mais atrasados primeiro.

    Por padrão a fila é limitada ao que falta para a meta diária do usuário;
    `include_all=true` devolve todos os vencidos (até `MAX_DUE_CARDS`).
    """
    today = today_in_study_tz()

    states = {
        state.card_id: state
        for state in db.scalars(
            select(ReviewState).where(ReviewState.user_id == current_user.id)
        )
    }

    cards = db.scalars(select(Card).where(_visible_to(current_user)).order_by(Card.id))

    due: list[DueCardOut] = []
    for card in cards:
        state = states.get(card.id)
        if state is not None and state.due_date > today:
            continue
        due.append(
            DueCardOut(
                id=card.id,
                front_pt=card.front_pt,
                back_de=card.back_de,
                phonetic_hint=card.phonetic_hint,
                category=card.category,
                owner_id=card.owner_id,
                created_at=card.created_at,
                due_date=state.due_date if state else None,
                interval_days=state.interval_days if state else 0,
                repetitions=state.repetitions if state else 0,
                ease_factor=state.ease_factor if state else 2.5,
                is_new=state is None,
            )
        )

    due.sort(key=lambda c: (c.due_date is not None, c.due_date or today))

    done_today = reviews_today(db, current_user.id)
    remaining_for_goal = max(0, current_user.daily_goal - done_today)
    cards = due if include_all else due[:remaining_for_goal]

    return DueCardsOut(
        daily_goal=current_user.daily_goal,
        reviewed_today=done_today,
        due_total=len(due),
        cards=cards[:MAX_DUE_CARDS],
    )


@router.post("", response_model=ReviewResult, status_code=status.HTTP_201_CREATED)
def submit_review(payload: ReviewCreate, db: DbSession, current_user: Writer):
    """Recalcula o intervalo do cartão pelo SM-2, grava o histórico e pontua."""
    card = db.get(Card, payload.card_id)
    if card is None or (card.owner_id is not None and card.owner_id != current_user.id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cartão não encontrado.")

    state = db.scalar(
        select(ReviewState).where(
            ReviewState.user_id == current_user.id,
            ReviewState.card_id == card.id,
        )
    )
    previous = (
        Sm2State(state.repetitions, state.ease_factor, state.interval_days)
        if state
        else initial_state()
    )

    updated = apply_sm2(previous, payload.grade)
    next_due = today_in_study_tz() + timedelta(days=updated.interval_days)
    now = datetime.now(timezone.utc)

    if state is None:
        state = ReviewState(user_id=current_user.id, card_id=card.id)
        db.add(state)
    state.repetitions = updated.repetitions
    state.ease_factor = updated.ease_factor
    state.interval_days = updated.interval_days
    state.due_date = next_due
    state.last_reviewed_at = now
    state.last_grade = payload.grade

    points = points_for_review(payload.grade)
    db.add(
        ReviewLog(
            user_id=current_user.id,
            card_id=card.id,
            grade=payload.grade,
            previous_interval=previous.interval_days,
            new_interval=updated.interval_days,
            ease_factor_after=updated.ease_factor,
            points_earned=points,
            reviewed_at=now,
        )
    )
    db.commit()

    return ReviewResult(
        card_id=card.id,
        grade=payload.grade,
        previous_interval=previous.interval_days,
        new_interval=updated.interval_days,
        next_due_date=next_due,
        ease_factor=updated.ease_factor,
        repetitions=updated.repetitions,
        points_earned=points,
    )
