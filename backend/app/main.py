"""Ponto de entrada do FastAPI: cria as tabelas, monta o CORS e os routers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine
from app.routers import auth, cards, dashboard, progress, reviews, scenarios

# Para um projeto deste tamanho, criar as tabelas na inicialização basta.
# Migrations (Alembic) entram quando o schema começar a evoluir em produção.
Base.metadata.create_all(bind=engine)


def _apply_pending_migrations() -> None:
    """Colunas adicionadas depois do deploy inicial. Provisório até entrar Alembic.

    Só roda no Postgres — no SQLite o banco é sempre recriado do zero pelo create_all.
    """
    if not settings.database_url.startswith("postgresql"):
        return
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url TEXT"))


_apply_pending_migrations()

if settings.seed_on_startup:
    from app.seed import run as seed_database

    seed_database()

app = FastAPI(
    title="Deutsch App API",
    description=(
        "API de estudo de alemão: flashcards com repetição espaçada (SM-2), "
        "cenários de burocracia em roleplay e dashboard de progresso do casal."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cards.router)
app.include_router(reviews.router)
app.include_router(scenarios.router)
app.include_router(dashboard.router)
app.include_router(progress.router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
