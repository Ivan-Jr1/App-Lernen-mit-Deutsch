"""Reset de progresso da conta logada.

Apaga o histórico que alimenta o placar (revisões e jogadas de cenário) mas
mantém a agenda de repetição espaçada (`review_states`) — o usuário não perde
os cartões que já aprendeu, só zera pontos, streak e contadores.
"""

from fastapi import APIRouter, status
from sqlalchemy import delete, select

from app.deps import DbSession, Writer
from app.models import ReviewLog, ScenarioAttempt

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_score(current_user: Writer, db: DbSession):
    # Cada jogada é apagada pelo ORM para o cascade remover também as respostas.
    for attempt in db.scalars(
        select(ScenarioAttempt).where(ScenarioAttempt.user_id == current_user.id)
    ):
        db.delete(attempt)

    db.execute(delete(ReviewLog).where(ReviewLog.user_id == current_user.id))
    db.commit()
