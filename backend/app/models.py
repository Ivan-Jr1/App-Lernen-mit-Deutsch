"""Modelos ORM (SQLAlchemy 2.0).

Regra central do domínio: um cartão guarda apenas o conteúdo. O progresso de
repetição espaçada (facilidade, intervalo, vencimento) vive em `ReviewState`,
uma linha por (usuário, cartão) — assim um cartão compartilhado tem agenda
independente para cada pessoa.
"""

from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    """Usuário do app. Contas criadas por seed: `ivan`, `gabriela` e o `demo`
    (visitante). Cadastro é fechado — não há criação de contas em runtime."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(100))
    # Nulo enquanto a conta não foi "reivindicada": no primeiro acesso o usuário
    # escolhe a própria senha. A conta de visitante permanece sempre nula.
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_guest: Mapped[bool] = mapped_column(Boolean, default=False)
    # Foto de perfil como data URI (o cliente já redimensiona antes de enviar).
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Quantos cartões o usuário quer revisar por dia. A fila de revisão é limitada
    # a esse número por padrão, para não assustar com pilhas grandes.
    daily_goal: Mapped[int] = mapped_column(Integer, default=20)
    # Idioma que o usuário está estudando agora (código ISO 639-1, ver
    # app/languages.py). A fila de revisão e a lista de cenários seguem este valor.
    learning_language: Mapped[str] = mapped_column(String(5), default="de")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    review_states: Mapped[list["ReviewState"]] = relationship(back_populates="user")
    review_logs: Mapped[list["ReviewLog"]] = relationship(back_populates="user")
    scenario_attempts: Mapped[list["ScenarioAttempt"]] = relationship(back_populates="user")


class Card(Base):
    """Conteúdo de um flashcard. Não guarda estado de estudo."""

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    front_pt: Mapped[str] = mapped_column(String(300))  # frente: frase em português
    back_target: Mapped[str] = mapped_column(String(300))  # verso: tradução no idioma estudado
    # idioma do verso (código ISO 639-1, ver app/languages.py)
    language: Mapped[str] = mapped_column(String(5), default="de", index=True)
    # aproximação de pronúncia em português, ex.: "Wie geht's" -> "Ví guêts"
    phonetic_hint: Mapped[str | None] = mapped_column(String(300), nullable=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    # NULL = cartão compartilhado (aparece para os dois usuários).
    # Preenchido = cartão privado daquele usuário.
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    owner: Mapped["User | None"] = relationship()


class ReviewState(Base):
    """Estado SM-2 atual de um cartão para um usuário.

    Criado no primeiro contato do usuário com o cartão. Enquanto não existir,
    o cartão é tratado como novo (vencido para revisão).
    """

    __tablename__ = "review_states"
    __table_args__ = (UniqueConstraint("user_id", "card_id", name="uq_review_state_user_card"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), index=True)

    repetitions: Mapped[int] = mapped_column(Integer, default=0)  # revisões seguidas com nota >= 3
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)  # EF do SM-2, mínimo 1.3
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    due_date: Mapped[date] = mapped_column(Date, index=True)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_grade: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user: Mapped["User"] = relationship(back_populates="review_states")
    card: Mapped["Card"] = relationship()


class ReviewLog(Base):
    """Registro imutável de uma revisão. Base para histórico, pontos e gráficos."""

    __tablename__ = "review_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), index=True)

    grade: Mapped[int] = mapped_column(Integer)  # nota informada, 0 a 5
    previous_interval: Mapped[int] = mapped_column(Integer)
    new_interval: Mapped[int] = mapped_column(Integer)
    ease_factor_after: Mapped[float] = mapped_column(Float)
    points_earned: Mapped[int] = mapped_column(Integer)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, index=True)

    user: Mapped["User"] = relationship(back_populates="review_logs")
    card: Mapped["Card"] = relationship()


class Scenario(Base):
    """Um cenário de burocracia (Anmeldung, abrir conta, alugar apartamento...)."""

    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(500))  # contexto mostrado antes de começar
    category: Mapped[str] = mapped_column(String(50))
    # idioma do diálogo (código ISO 639-1, ver app/languages.py)
    language: Mapped[str] = mapped_column(String(5), default="de", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    steps: Mapped[list["ScenarioStep"]] = relationship(
        back_populates="scenario",
        order_by="ScenarioStep.step_order",
        cascade="all, delete-orphan",
    )


class ScenarioStep(Base):
    """Uma fala do atendente dentro de um cenário, com suas opções de resposta."""

    __tablename__ = "scenario_steps"
    __table_args__ = (UniqueConstraint("scenario_id", "step_order", name="uq_step_scenario_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), index=True)
    step_order: Mapped[int] = mapped_column(Integer)  # 1, 2, 3...
    speaker_text_target: Mapped[str] = mapped_column(String(500))  # fala do atendente no idioma estudado
    speaker_text_pt: Mapped[str | None] = mapped_column(String(500), nullable=True)  # tradução de apoio

    scenario: Mapped["Scenario"] = relationship(back_populates="steps")
    options: Mapped[list["ScenarioOption"]] = relationship(
        back_populates="step",
        order_by="ScenarioOption.option_order",
        cascade="all, delete-orphan",
    )


class ScenarioOption(Base):
    """Uma opção de resposta de múltipla escolha para um passo."""

    __tablename__ = "scenario_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    step_id: Mapped[int] = mapped_column(ForeignKey("scenario_steps.id"), index=True)
    option_text_target: Mapped[str] = mapped_column(String(400))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)  # exatamente uma por passo
    # por que a resposta correta é mais natural — mostrado ao errar
    explanation: Mapped[str] = mapped_column(String(600))
    option_order: Mapped[int] = mapped_column(Integer)

    step: Mapped["ScenarioStep"] = relationship(back_populates="options")


class ScenarioAttempt(Base):
    """Uma jogada de um cenário por um usuário."""

    __tablename__ = "scenario_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), index=True)

    total_steps: Mapped[int] = mapped_column(Integer)  # nº de passos no momento da jogada
    correct_count: Mapped[int] = mapped_column(Integer, default=0)  # acertos na primeira tentativa
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="scenario_attempts")
    scenario: Mapped["Scenario"] = relationship()
    answers: Mapped[list["ScenarioAttemptAnswer"]] = relationship(
        back_populates="attempt",
        cascade="all, delete-orphan",
    )


class ScenarioAttemptAnswer(Base):
    """Resposta escolhida em um passo de uma jogada. Permite revisar os erros depois."""

    __tablename__ = "scenario_attempt_answers"
    __table_args__ = (UniqueConstraint("attempt_id", "step_id", name="uq_answer_attempt_step"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("scenario_attempts.id"), index=True)
    step_id: Mapped[int] = mapped_column(ForeignKey("scenario_steps.id"))
    option_id: Mapped[int] = mapped_column(ForeignKey("scenario_options.id"))
    is_correct: Mapped[bool] = mapped_column(Boolean)  # cópia do acerto no momento da resposta
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    attempt: Mapped["ScenarioAttempt"] = relationship(back_populates="answers")
