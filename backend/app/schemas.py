"""Schemas Pydantic para request e response. Separam o contrato da API dos
modelos ORM."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

# --------------------------------------------------------------------------- #
# Autenticação                                                                 #
# --------------------------------------------------------------------------- #


class AccountOut(BaseModel):
    """Uma das contas fixas, com o aviso de se já tem senha definida."""

    username: str
    display_name: str
    claimed: bool  # False = ainda vai definir a senha no primeiro acesso


class Credentials(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class AuthUser(BaseModel):
    username: str
    display_name: str
    readonly: bool


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser

# --------------------------------------------------------------------------- #
# Cartões                                                                      #
# --------------------------------------------------------------------------- #


class CardBase(BaseModel):
    front_pt: str = Field(min_length=1, max_length=300)
    back_de: str = Field(min_length=1, max_length=300)
    phonetic_hint: str | None = Field(default=None, max_length=300)
    category: str | None = Field(default=None, max_length=50)


class CardCreate(CardBase):
    # username do dono para um cartão privado; ausente = cartão compartilhado
    owner_username: str | None = None


class CardUpdate(BaseModel):
    front_pt: str | None = Field(default=None, min_length=1, max_length=300)
    back_de: str | None = Field(default=None, min_length=1, max_length=300)
    phonetic_hint: str | None = Field(default=None, max_length=300)
    category: str | None = Field(default=None, max_length=50)


class CardOut(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None
    created_at: datetime


class DueCardOut(CardOut):
    """Cartão vencido, com o estado SRS do usuário anexado (None se for novo)."""

    due_date: date | None
    interval_days: int
    repetitions: int
    ease_factor: float
    is_new: bool


# --------------------------------------------------------------------------- #
# Revisões                                                                     #
# --------------------------------------------------------------------------- #


class ReviewCreate(BaseModel):
    card_id: int
    grade: int = Field(ge=0, le=5)


class ReviewResult(BaseModel):
    card_id: int
    grade: int
    previous_interval: int
    new_interval: int
    next_due_date: date
    ease_factor: float
    repetitions: int
    points_earned: int


# --------------------------------------------------------------------------- #
# Cenários                                                                     #
# --------------------------------------------------------------------------- #


class ScenarioOptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    option_text_de: str
    option_order: int
    # is_correct e explanation são omitidos de propósito: o cliente só descobre
    # ao responder (POST .../answers).


class ScenarioStepOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    step_order: int
    speaker_text_de: str
    speaker_text_pt: str | None
    options: list[ScenarioOptionOut]


class ScenarioSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    category: str


class ScenarioDetailOut(ScenarioSummaryOut):
    steps: list[ScenarioStepOut]


class AttemptStart(BaseModel):
    scenario_slug: str


class AnswerCreate(BaseModel):
    step_id: int
    option_id: int


class AnswerResult(BaseModel):
    step_id: int
    chosen_option_id: int
    is_correct: bool
    correct_option_id: int
    explanation: str
    attempt_completed: bool
    points_earned: int | None  # preenchido só quando a jogada é concluída


class AttemptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_id: int
    total_steps: int
    correct_count: int
    is_completed: bool
    points_earned: int
    started_at: datetime
    completed_at: datetime | None


# --------------------------------------------------------------------------- #
# Dashboard                                                                    #
# --------------------------------------------------------------------------- #


class UserProgress(BaseModel):
    username: str
    display_name: str
    total_points: int
    current_streak: int
    longest_streak: int
    total_cards_reviewed: int
    scenarios_completed: int
    cards_due_today: int


class DashboardOut(BaseModel):
    users: list[UserProgress]
