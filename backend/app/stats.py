"""Cálculo de streak e agregados do dashboard.

Tudo é derivado de `review_logs` e `scenario_attempts` — não há tabela de placar.
Um "dia de estudo" é qualquer dia (no fuso de `study_timezone`) com ao menos uma
revisão ou um cenário concluído.
"""

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import ReviewLog, ScenarioAttempt


def _local_date(moment: datetime, tz: ZoneInfo) -> date:
    # SQLite devolve datetimes sem tzinfo; tratamos o valor gravado como UTC.
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(tz).date()


def study_days(db: Session, user_id: int) -> set[date]:
    """Conjunto de dias em que o usuário estudou algo."""
    tz = ZoneInfo(settings.study_timezone)
    days: set[date] = set()

    for moment in db.scalars(select(ReviewLog.reviewed_at).where(ReviewLog.user_id == user_id)):
        days.add(_local_date(moment, tz))

    completed_at = select(ScenarioAttempt.completed_at).where(
        ScenarioAttempt.user_id == user_id,
        ScenarioAttempt.is_completed.is_(True),
    )
    for moment in db.scalars(completed_at):
        if moment is not None:
            days.add(_local_date(moment, tz))

    return days


def today_in_study_tz() -> date:
    return datetime.now(ZoneInfo(settings.study_timezone)).date()


def reviews_today(db: Session, user_id: int) -> int:
    """Quantas revisões o usuário registrou hoje (no fuso de estudo)."""
    tz = ZoneInfo(settings.study_timezone)
    today = today_in_study_tz()
    moments = db.scalars(select(ReviewLog.reviewed_at).where(ReviewLog.user_id == user_id))
    return sum(1 for moment in moments if _local_date(moment, tz) == today)


def current_streak(days: set[date], today: date) -> int:
    """Dias consecutivos terminando hoje (ou ontem, se ainda não estudou hoje)."""
    anchor = today if today in days else today - timedelta(days=1)
    streak = 0
    while anchor in days:
        streak += 1
        anchor -= timedelta(days=1)
    return streak


def longest_streak(days: set[date]) -> int:
    """Maior sequência de dias de estudo consecutivos no histórico."""
    if not days:
        return 0

    ordered = sorted(days)
    best = run = 1
    for previous, current in zip(ordered, ordered[1:]):
        run = run + 1 if current - previous == timedelta(days=1) else 1
        best = max(best, run)
    return best
