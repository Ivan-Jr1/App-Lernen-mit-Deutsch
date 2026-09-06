"""Cenários de burocracia em roleplay de múltipla escolha e as jogadas do usuário."""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.deps import CurrentUser, DbSession
from app.models import (
    Scenario,
    ScenarioAttempt,
    ScenarioAttemptAnswer,
    ScenarioOption,
    ScenarioStep,
)
from app.schemas import (
    AnswerCreate,
    AnswerResult,
    AttemptOut,
    ScenarioDetailOut,
    ScenarioSummaryOut,
)
from app.scoring import points_for_scenario

router = APIRouter(prefix="/api", tags=["scenarios"])


def _get_scenario_by_slug(db: DbSession, slug: str) -> Scenario:
    scenario = db.scalar(select(Scenario).where(Scenario.slug == slug))
    if scenario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cenário não encontrado.")
    return scenario


@router.get("/scenarios", response_model=list[ScenarioSummaryOut])
def list_scenarios(db: DbSession):
    return list(db.scalars(select(Scenario).order_by(Scenario.id)))


@router.get("/scenarios/{slug}", response_model=ScenarioDetailOut)
def get_scenario(slug: str, db: DbSession):
    return _get_scenario_by_slug(db, slug)


@router.post(
    "/scenarios/{slug}/attempts",
    response_model=AttemptOut,
    status_code=status.HTTP_201_CREATED,
)
def start_attempt(slug: str, db: DbSession, current_user: CurrentUser):
    scenario = _get_scenario_by_slug(db, slug)
    attempt = ScenarioAttempt(
        user_id=current_user.id,
        scenario_id=scenario.id,
        total_steps=len(scenario.steps),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


@router.post("/attempts/{attempt_id}/answers", response_model=AnswerResult)
def answer_step(
    attempt_id: int,
    payload: AnswerCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    attempt = db.get(ScenarioAttempt, attempt_id)
    if attempt is None or attempt.user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Jogada não encontrada.")
    if attempt.is_completed:
        raise HTTPException(status.HTTP_409_CONFLICT, "Esta jogada já foi concluída.")

    step = db.get(ScenarioStep, payload.step_id)
    if step is None or step.scenario_id != attempt.scenario_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Passo não pertence a este cenário.")

    chosen = db.get(ScenarioOption, payload.option_id)
    if chosen is None or chosen.step_id != step.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Opção não pertence a este passo.")

    already_answered = db.scalar(
        select(ScenarioAttemptAnswer).where(
            ScenarioAttemptAnswer.attempt_id == attempt.id,
            ScenarioAttemptAnswer.step_id == step.id,
        )
    )
    if already_answered is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Este passo já foi respondido.")

    correct_option = next(option for option in step.options if option.is_correct)
    is_correct = chosen.id == correct_option.id

    db.add(
        ScenarioAttemptAnswer(
            attempt_id=attempt.id,
            step_id=step.id,
            option_id=chosen.id,
            is_correct=is_correct,
        )
    )
    if is_correct:
        attempt.correct_count += 1
    db.flush()

    answered_steps = db.scalars(
        select(ScenarioAttemptAnswer.step_id).where(
            ScenarioAttemptAnswer.attempt_id == attempt.id
        )
    ).all()

    points: int | None = None
    just_completed = len(answered_steps) >= attempt.total_steps
    if just_completed:
        attempt.is_completed = True
        attempt.completed_at = datetime.now(timezone.utc)
        points = points_for_scenario(attempt.correct_count, attempt.total_steps)
        attempt.points_earned = points

    db.commit()

    return AnswerResult(
        step_id=step.id,
        chosen_option_id=chosen.id,
        is_correct=is_correct,
        correct_option_id=correct_option.id,
        explanation=correct_option.explanation,
        attempt_completed=just_completed,
        points_earned=points,
    )


@router.get("/attempts/{attempt_id}", response_model=AttemptOut)
def get_attempt(attempt_id: int, db: DbSession, current_user: CurrentUser):
    attempt = db.get(ScenarioAttempt, attempt_id)
    if attempt is None or attempt.user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Jogada não encontrada.")
    return attempt
