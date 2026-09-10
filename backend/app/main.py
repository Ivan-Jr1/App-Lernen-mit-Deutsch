"""Ponto de entrada do FastAPI: cria as tabelas, monta o CORS e os routers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine
from app.routers import auth, cards, dashboard, languages, progress, reviews, scenarios

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
        connection.execute(
            text("ALTER TABLE users ADD COLUMN IF NOT EXISTS daily_goal INTEGER NOT NULL DEFAULT 20")
        )
        # Segunda língua: idioma por cartão/cenário e o idioma ativo de cada conta.
        connection.execute(
            text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS "
                "learning_language VARCHAR(5) NOT NULL DEFAULT 'de'"
            )
        )
        connection.execute(
            text("ALTER TABLE cards ADD COLUMN IF NOT EXISTS language VARCHAR(5) NOT NULL DEFAULT 'de'")
        )
        connection.execute(
            text(
                "ALTER TABLE scenarios ADD COLUMN IF NOT EXISTS "
                "language VARCHAR(5) NOT NULL DEFAULT 'de'"
            )
        )
        # Renomeia as colunas de conteúdo `_de` para nomes neutros de idioma.
        # Postgres não aceita "RENAME COLUMN IF EXISTS", então cada rename é
        # protegido por uma checagem no information_schema (idempotente).
        for table, old_column, new_column in (
            ("cards", "back_de", "back_target"),
            ("scenario_steps", "speaker_text_de", "speaker_text_target"),
            ("scenario_options", "option_text_de", "option_text_target"),
        ):
            connection.execute(
                text(
                    f"DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns "
                    f"WHERE table_name = '{table}' AND column_name = '{old_column}') "
                    f"THEN ALTER TABLE {table} RENAME COLUMN {old_column} TO {new_column}; "
                    f"END IF; END $$;"
                )
            )


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
app.include_router(languages.router)
app.include_router(cards.router)
app.include_router(reviews.router)
app.include_router(scenarios.router)
app.include_router(dashboard.router)
app.include_router(progress.router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
