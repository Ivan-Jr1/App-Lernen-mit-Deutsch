"""Configuração da aplicação, lida de variáveis de ambiente (ou de um .env)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # URL do banco. SQLite por padrão; troque por uma URL postgresql://... sem
    # mudar mais nada no código.
    database_url: str = "sqlite:///./deutsch.db"

    # Fuso usado para decidir o que conta como "dia de estudo" no streak.
    # Berlim é o destino da mudança, então é o fuso de referência.
    study_timezone: str = "Europe/Berlin"

    # No Render free tier o disco é efêmero e o SQLite é zerado a cada deploy.
    # Ligue isto em produção para o banco ser repovoado na inicialização.
    seed_on_startup: bool = False

    # Origens liberadas no CORS (o front local do Vite e, depois, o domínio de produção).
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
