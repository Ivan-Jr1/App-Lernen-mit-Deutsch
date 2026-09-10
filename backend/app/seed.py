"""Popula o banco com os dados de exemplo.

Uso:
    python -m app.seed          # cria o que faltar (não duplica)
    python -m app.seed --reset  # apaga tudo e recria do zero
"""

import sys
from datetime import datetime, timedelta, timezone

from sqlalchemy import or_, select

from app.data.seed_data import (
    CARDS,
    DEMO_REVIEW_GRADES,
    DEMO_SCENARIOS_DONE,
    SCENARIOS,
    USERS,
)
from app.database import Base, SessionLocal, engine
from app.models import (
    Card,
    ReviewLog,
    ReviewState,
    Scenario,
    ScenarioAttempt,
    ScenarioAttemptAnswer,
    ScenarioOption,
    ScenarioStep,
    User,
)
from app.scoring import points_for_review, points_for_scenario
from app.srs import Sm2State, initial_state, review as apply_sm2
from app.stats import today_in_study_tz


def _seed_users(db) -> dict[str, User]:
    users: dict[str, User] = {}
    for row in USERS:
        user = db.scalar(select(User).where(User.username == row["username"]))
        if user is None:
            user = User(
                username=row["username"],
                display_name=row["display_name"],
                is_guest=row["is_guest"],
            )
            db.add(user)
            db.flush()
        users[user.username] = user
    return users


def _seed_cards(db, users: dict[str, User]) -> None:
    for row in CARDS:
        language = row.get("language", "de")  # linhas sem a chave são do deck alemão
        exists = db.scalar(
            select(Card).where(
                Card.front_pt == row["front_pt"],
                Card.back_target == row["back_target"],
                Card.language == language,
            )
        )
        if exists:
            continue
        owner_id = users[row["owner"]].id if row["owner"] else None
        db.add(
            Card(
                front_pt=row["front_pt"],
                back_target=row["back_target"],
                language=language,
                phonetic_hint=row["phonetic_hint"],
                category=row["category"],
                owner_id=owner_id,
            )
        )


def _seed_scenarios(db) -> None:
    for row in SCENARIOS:
        if db.scalar(select(Scenario).where(Scenario.slug == row["slug"])):
            continue
        scenario = Scenario(
            slug=row["slug"],
            title=row["title"],
            description=row["description"],
            category=row["category"],
            language=row.get("language", "de"),
        )
        db.add(scenario)
        db.flush()

        for step_index, step_row in enumerate(row["steps"], start=1):
            step = ScenarioStep(
                scenario_id=scenario.id,
                step_order=step_index,
                speaker_text_target=step_row["speaker_target"],
                speaker_text_pt=step_row.get("speaker_pt"),
            )
            db.add(step)
            db.flush()
            for option_index, option_row in enumerate(step_row["options"], start=1):
                db.add(
                    ScenarioOption(
                        step_id=step.id,
                        option_text_target=option_row["text_target"],
                        is_correct=option_row["correct"],
                        explanation=option_row["explanation"],
                        option_order=option_index,
                    )
                )


def _review_card(db, user: User, card: Card, grade: int, now: datetime) -> None:
    """Aplica uma revisão SM-2 (mesma lógica do endpoint) e grava o log."""
    previous = initial_state()
    updated = apply_sm2(previous, grade)
    db.add(
        ReviewState(
            user_id=user.id,
            card_id=card.id,
            repetitions=updated.repetitions,
            ease_factor=updated.ease_factor,
            interval_days=updated.interval_days,
            due_date=today_in_study_tz() + timedelta(days=updated.interval_days),
            last_reviewed_at=now,
            last_grade=grade,
        )
    )
    db.add(
        ReviewLog(
            user_id=user.id,
            card_id=card.id,
            grade=grade,
            previous_interval=previous.interval_days,
            new_interval=updated.interval_days,
            ease_factor_after=updated.ease_factor,
            points_earned=points_for_review(grade),
            reviewed_at=now,
        )
    )


def _complete_scenario(db, user: User, scenario: Scenario, now: datetime) -> None:
    """Cria uma jogada concluída acertando todos os passos."""
    attempt = ScenarioAttempt(
        user_id=user.id,
        scenario_id=scenario.id,
        total_steps=len(scenario.steps),
        correct_count=len(scenario.steps),
        is_completed=True,
        points_earned=points_for_scenario(len(scenario.steps), len(scenario.steps)),
        started_at=now,
        completed_at=now,
    )
    db.add(attempt)
    db.flush()
    for step in scenario.steps:
        correct = next(option for option in step.options if option.is_correct)
        db.add(
            ScenarioAttemptAnswer(
                attempt_id=attempt.id,
                step_id=step.id,
                option_id=correct.id,
                is_correct=True,
                answered_at=now,
            )
        )


def _seed_demo_activity(db, users: dict[str, User]) -> None:
    """Atividade de exemplo para a demo não parecer vazia. Roda só uma vez."""
    if db.scalar(select(ReviewLog.id).limit(1)) is not None:
        return

    now = datetime.now(timezone.utc)

    for username, grades in DEMO_REVIEW_GRADES.items():
        user = users[username]
        visible_cards = db.scalars(
            select(Card)
            .where(or_(Card.owner_id.is_(None), Card.owner_id == user.id))
            .order_by(Card.id)
        ).all()
        for card, grade in zip(visible_cards, grades):
            _review_card(db, user, card, grade, now)

    for username, slugs in DEMO_SCENARIOS_DONE.items():
        for slug in slugs:
            scenario = db.scalar(select(Scenario).where(Scenario.slug == slug))
            if scenario is not None:
                _complete_scenario(db, users[username], scenario, now)


def run(reset: bool = False) -> None:
    if reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        users = _seed_users(db)
        _seed_cards(db, users)
        _seed_scenarios(db)
        db.flush()
        _seed_demo_activity(db, users)
        db.commit()

    print("Seed concluído.")


if __name__ == "__main__":
    run(reset="--reset" in sys.argv)
