"""Schemas Pydantic para request e response. Separam o contrato da API dos
modelos ORM."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.languages import SUPPORTED_LANGUAGES

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
    avatar_url: str | None = None
    daily_goal: int = 20
    learning_language: str = "de"


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=60)
    # data URI de imagem (ex.: "data:image/jpeg;base64,...") ou null para remover.
    # Limite generoso: o cliente redimensiona para ~256px antes de enviar.
    avatar_url: str | None = Field(default=None, max_length=350_000)
    daily_goal: int | None = Field(default=None, ge=1, le=200)
    learning_language: str | None = None

    @field_validator("learning_language")
    @classmethod
    def _known_language(cls, value: str | None) -> str | None:
        if value is not None and value not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Idioma não suportado: {value}")
        return value


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)


# --------------------------------------------------------------------------- #
# Idiomas                                                                      #
# --------------------------------------------------------------------------- #


class LanguageOut(BaseModel):
    code: str  # ISO 639-1, ex.: "de"
    name: str  # nome de exibição, ex.: "Alemão"

# --------------------------------------------------------------------------- #
# Cartões                                                                      #
# --------------------------------------------------------------------------- #


class CardBase(BaseModel):
    front_pt: str = Field(min_length=1, max_length=300)
    back_target: str = Field(min_length=1, max_length=300)
    phonetic_hint: str | None = Field(default=None, max_length=300)
    category: str | None = Field(default=None, max_length=50)


class CardCreate(CardBase):
    # username do dono para um cartão privado; ausente = cartão compartilhado
    owner_username: str | None = None
    # idioma do cartão; ausente = o idioma que o criador está estudando
    language: str | None = None


class CardUpdate(BaseModel):
    front_pt: str | None = Field(default=None, min_length=1, max_length=300)
    back_target: str | None = Field(default=None, min_length=1, max_length=300)
    phonetic_hint: str | None = Field(default=None, max_length=300)
    category: str | None = Field(default=None, max_length=50)


class CardOut(CardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None
    language: str
    created_at: datetime


class DueCardOut(CardOut):
    """Cartão vencido, com o estado SRS do usuário anexado (None se for novo)."""

    due_date: date | None
    interval_days: int
    repetitions: int
    ease_factor: float
    is_new: bool


class DueCardsOut(BaseModel):
    """Fila de revisão do dia mais o progresso em relação à meta diária."""

    daily_goal: int
    reviewed_today: int
    due_total: int  # total de cartões vencidos, ignorando o limite da meta
    cards: list[DueCardOut]  # já limitado à meta, salvo quando include_all=true


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
    option_text_target: str
    option_order: int
    # is_correct e explanation são omitidos de propósito: o cliente só descobre
    # ao responder (POST .../answers).


class ScenarioStepOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    step_order: int
    speaker_text_target: str
    speaker_text_pt: str | None
    options: list[ScenarioOptionOut]


class ScenarioSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    category: str
    language: str


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
    reviewed_today: int
    daily_goal: int


class DashboardOut(BaseModel):
    users: list[UserProgress]
