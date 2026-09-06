"""Dashboard do casal: progresso dos dois usuários lado a lado."""

from fastapi import APIRouter
from sqlalchemy import func, or_, select

from app.deps import DbSession
from app.models import Card, ReviewLog, ReviewState, ScenarioAttempt, User
from app.schemas import DashboardOut, UserProgress
from app.stats import (
    current_streak,
    longest_streak,
    study_days,
    today_in_study_tz,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def _cards_due_today(db: DbSession, user: User, today) -> int:
    """Cartões visíveis ao usuário que estão vencidos ou nunca foram vistos."""
    visible = select(Card.id).where(or_(Card.owner_id.is_(None), Card.owner_id == user.id))

    seen_and_not_due = select(func.count(ReviewState.id)).where(
        ReviewState.user_id == user.id,
        ReviewState.card_id.in_(visible),
        ReviewState.due_date > today,
    )
    total_visible = db.scalar(select(func.count()).select_from(visible.subquery()))
    not_due = db.scalar(seen_and_not_due)
    return total_visible - not_due


@router.get("", response_model=DashboardOut)
def get_dashboard(db: DbSession):
    today = today_in_study_tz()
    progress: list[UserProgress] = []

    for user in db.scalars(select(User).order_by(User.id)):
        days = study_days(db, user.id)

        review_points = db.scalar(
            select(func.coalesce(func.sum(ReviewLog.points_earned), 0)).where(
                ReviewLog.user_id == user.id
            )
        )
        scenario_points = db.scalar(
            select(func.coalesce(func.sum(ScenarioAttempt.points_earned), 0)).where(
                ScenarioAttempt.user_id == user.id,
                ScenarioAttempt.is_completed.is_(True),
            )
        )
        cards_reviewed = db.scalar(
            select(func.count(ReviewLog.id)).where(ReviewLog.user_id == user.id)
        )
        scenarios_completed = db.scalar(
            select(func.count(ScenarioAttempt.id)).where(
                ScenarioAttempt.user_id == user.id,
                ScenarioAttempt.is_completed.is_(True),
            )
        )

        progress.append(
            UserProgress(
                username=user.username,
                display_name=user.display_name,
                total_points=review_points + scenario_points,
                current_streak=current_streak(days, today),
                longest_streak=longest_streak(days),
                total_cards_reviewed=cards_reviewed,
                scenarios_completed=scenarios_completed,
                cards_due_today=_cards_due_today(db, user, today),
            )
        )

    return DashboardOut(users=progress)
