"""Configuração da aplicação, lida de variáveis de ambiente (ou de um .env)."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # URL do banco. SQLite por padrão; basta trocar por uma URL postgresql://...
    # (Neon, Supabase, Render Postgres) — nada mais no código muda.
    database_url: str = "sqlite:///./deutsch.db"

    @field_validator("database_url")
    @classmethod
    def _use_psycopg3_driver(cls, value: str) -> str:
        # Provedores entregam "postgresql://"; o SQLAlchemy assumiria psycopg2.
        # Forçamos o psycopg 3, que é o que está no requirements.
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    # Fuso usado para decidir o que conta como "dia de estudo" no streak.
    # Berlim é o destino da mudança, então é o fuso de referência.
    study_timezone: str = "Europe/Berlin"

    # Popula o banco na inicialização. Os seeders são idempotentes, então é
    # seguro deixar ligado mesmo com Postgres persistente (vira no-op após a 1ª vez).
    seed_on_startup: bool = False

    # Chave de assinatura dos tokens JWT. O default só serve para desenvolvimento
    # local — em produção defina JWT_SECRET com um valor aleatório longo.
    jwt_secret: str = "dev-secret-change-me-in-production-please"
    jwt_expire_days: int = 30  # app pessoal em celular: sessão longa é aceitável

    # Origens liberadas no CORS (o front local do Vite).
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # A Vercel dá uma URL única por deploy (previews), então liberamos qualquer
    # subdomínio *.vercel.app por regex em vez de listar uma a uma.
    cors_origin_regex: str = r"https://.*\.vercel\.app"


settings = Settings()
