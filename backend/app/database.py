"""Engine do SQLAlchemy, fábrica de sessões e a dependência get_db do FastAPI."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

_is_sqlite = settings.database_url.startswith("sqlite")
_is_postgres = settings.database_url.startswith("postgresql")

if _is_sqlite:
    # check_same_thread só é aceito pelo SQLite; testes e Uvicorn usam threads diferentes.
    _connect_args = {"check_same_thread": False}
    _engine_kwargs = {}
elif _is_postgres:
    # O endpoint "pooled" do Neon é um pgBouncer em modo transaction, que quebra
    # com prepared statements — prepare_threshold=None desliga isso no psycopg.
    _connect_args = {"prepare_threshold": None}
    # pool_pre_ping evita erros de conexão morta após o Neon/Render hibernar.
    _engine_kwargs = {"pool_pre_ping": True}
else:
    _connect_args = {}
    _engine_kwargs = {}

engine = create_engine(settings.database_url, connect_args=_connect_args, **_engine_kwargs)
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
