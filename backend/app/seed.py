"""Popula o banco com os dados de exemplo.

Uso:
    python -m app.seed          # cria o que faltar (não duplica)
    python -m app.seed --reset  # apaga tudo e recria do zero
"""

import sys

from sqlalchemy import select

from app.data.seed_data import CARDS, SCENARIOS, USERS
from app.database import Base, SessionLocal, engine
from app.models import Card, Scenario, ScenarioOption, ScenarioStep, User


def _seed_users(db) -> dict[str, User]:
    users: dict[str, User] = {}
    for row in USERS:
        user = db.scalar(select(User).where(User.username == row["username"]))
        if user is None:
            user = User(username=row["username"], display_name=row["display_name"])
            db.add(user)
            db.flush()
        users[user.username] = user
    return users


def _seed_cards(db, users: dict[str, User]) -> None:
    for row in CARDS:
        exists = db.scalar(
            select(Card).where(Card.front_pt == row["front_pt"], Card.back_de == row["back_de"])
        )
        if exists:
            continue
        owner_id = users[row["owner"]].id if row["owner"] else None
        db.add(
            Card(
                front_pt=row["front_pt"],
                back_de=row["back_de"],
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
        )
        db.add(scenario)
        db.flush()

        for step_index, step_row in enumerate(row["steps"], start=1):
            step = ScenarioStep(
                scenario_id=scenario.id,
                step_order=step_index,
                speaker_text_de=step_row["speaker_de"],
                speaker_text_pt=step_row.get("speaker_pt"),
            )
            db.add(step)
            db.flush()
            for option_index, option_row in enumerate(step_row["options"], start=1):
                db.add(
                    ScenarioOption(
                        step_id=step.id,
                        option_text_de=option_row["text_de"],
                        is_correct=option_row["correct"],
                        explanation=option_row["explanation"],
                        option_order=option_index,
                    )
                )


def run(reset: bool = False) -> None:
    if reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        users = _seed_users(db)
        _seed_cards(db, users)
        _seed_scenarios(db)
        db.commit()

    print("Seed concluído.")


if __name__ == "__main__":
    run(reset="--reset" in sys.argv)
