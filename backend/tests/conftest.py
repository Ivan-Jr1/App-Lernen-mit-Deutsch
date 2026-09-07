"""Fixtures dos testes: um banco SQLite em memória isolado por teste, um
TestClient com a sessão sobrescrita e helpers de autenticação."""

import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET", "test-secret-not-used-in-production-0123456789")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Card, Scenario, ScenarioOption, ScenarioStep, User

TEST_PASSWORD = "senha-de-teste"


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # mantém uma única conexão -> o :memory: sobrevive entre requests
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def seeded(db_session: Session) -> dict:
    """Duas contas sem senha (claimáveis), um visitante, dois cartões e um
    cenário de dois passos."""
    db_session.add_all(
        [
            User(username="ivan", display_name="Ivan", is_guest=False),
            User(username="esposa", display_name="Esposa", is_guest=False),
            User(username="demo", display_name="Visitante", is_guest=True),
        ]
    )

    db_session.add_all(
        [
            Card(front_pt="Obrigado", back_de="Danke", phonetic_hint="Dânke", category="básico"),
            Card(front_pt="Sim / Não", back_de="Ja / Nein", phonetic_hint="Iá / Náin", category="básico"),
        ]
    )

    scenario = Scenario(
        slug="anmeldung",
        title="Anmeldung",
        description="Registro de endereço.",
        category="registro",
    )
    db_session.add(scenario)
    db_session.flush()

    for order, prompt in enumerate(["Was kann ich für Sie tun?", "Haben Sie das Formular?"], start=1):
        step = ScenarioStep(
            scenario_id=scenario.id,
            step_order=order,
            speaker_text_de=prompt,
            speaker_text_pt=None,
        )
        db_session.add(step)
        db_session.flush()
        db_session.add_all(
            [
                ScenarioOption(
                    step_id=step.id,
                    option_text_de="Resposta certa",
                    is_correct=True,
                    explanation="É a forma natural.",
                    option_order=1,
                ),
                ScenarioOption(
                    step_id=step.id,
                    option_text_de="Resposta errada",
                    is_correct=False,
                    explanation="Soa estranho.",
                    option_order=2,
                ),
            ]
        )

    db_session.commit()
    return {"scenario_slug": "anmeldung"}


@pytest.fixture
def token(client: TestClient, seeded: dict):
    """Devolve um token de acesso para uma conta, criando a senha na primeira vez."""

    def _token(username: str = "ivan", password: str = TEST_PASSWORD) -> str:
        response = client.post(
            "/api/auth/claim", json={"username": username, "password": password}
        )
        if response.status_code == 409:  # já tem senha -> login
            response = client.post(
                "/api/auth/login", json={"username": username, "password": password}
            )
        return response.json()["access_token"]

    return _token


@pytest.fixture
def auth(token):
    """Monta o header Authorization para uma conta."""

    def _headers(username: str = "ivan") -> dict[str, str]:
        return {"Authorization": f"Bearer {token(username)}"}

    return _headers


@pytest.fixture
def guest_headers(client: TestClient, seeded: dict) -> dict[str, str]:
    response = client.post("/api/auth/guest")
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
