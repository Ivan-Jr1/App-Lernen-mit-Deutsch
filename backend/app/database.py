"""Engine do SQLAlchemy, fábrica de sessões e a dependência get_db do FastAPI."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# check_same_thread só faz sentido (e só é aceito) no SQLite; o servidor de
# testes e o Uvicorn acessam a conexão de threads diferentes.
_connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(settings.database_url, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Classe base de todos os modelos ORM."""


def get_db() -> Iterator[Session]:
    """Abre uma sessão por request e garante o fechamento ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
