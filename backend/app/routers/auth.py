"""Autenticação e perfil: contas fixas, senha no primeiro acesso, login, visitante
(somente leitura), troca de senha e foto de perfil.

Cadastro é fechado — só existem as contas criadas pelo seed.
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.auth import create_access_token, hash_password, verify_password
from app.deps import DbSession, Reader, Writer
from app.models import User
from app.schemas import (
    AccountOut,
    AuthUser,
    Credentials,
    PasswordChange,
    ProfileUpdate,
    TokenOut,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _as_auth_user(user: User, *, readonly: bool) -> AuthUser:
    return AuthUser(
        username=user.username,
        display_name=user.display_name,
        readonly=readonly,
        avatar_url=user.avatar_url,
        daily_goal=user.daily_goal,
    )


def _token_response(user: User, *, readonly: bool) -> TokenOut:
    return TokenOut(
        access_token=create_access_token(user.id, user.username, readonly=readonly),
        user=_as_auth_user(user, readonly=readonly),
    )


@router.get("/accounts", response_model=list[AccountOut])
def list_accounts(db: DbSession):
    """Contas disponíveis para login, e se cada uma já definiu senha."""
    accounts = db.scalars(select(User).where(User.is_guest.is_(False)).order_by(User.id))
    return [
        AccountOut(
            username=user.username,
            display_name=user.display_name,
            claimed=user.password_hash is not None,
        )
        for user in accounts
    ]


@router.post("/claim", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def claim_account(payload: Credentials, db: DbSession):
    """Define a senha de uma conta que ainda não tem — só funciona uma vez."""
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or user.is_guest:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conta não encontrada.")
    if user.password_hash is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Esta conta já tem senha. Faça login.")

    user.password_hash = hash_password(payload.password)
    db.commit()
    return _token_response(user, readonly=False)


@router.post("/login", response_model=TokenOut)
def login(payload: Credentials, db: DbSession):
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or user.is_guest or user.password_hash is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário ou senha inválidos.")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário ou senha inválidos.")
    return _token_response(user, readonly=False)


@router.post("/guest", response_model=TokenOut)
def guest_access(db: DbSession):
    """Token somente leitura para recrutadores navegarem pelo app."""
    guest = db.scalar(select(User).where(User.is_guest.is_(True)))
    if guest is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Acesso de visitante indisponível.")
    return _token_response(guest, readonly=True)


@router.get("/me", response_model=AuthUser)
def me(current_user: Reader):
    # O token de visitante é o único readonly; is_guest é um proxy fiel disso.
    return _as_auth_user(current_user, readonly=current_user.is_guest)


@router.patch("/me", response_model=AuthUser)
def update_profile(payload: ProfileUpdate, current_user: Writer, db: DbSession):
    """Atualiza nome de exibição e/ou foto de perfil da conta logada."""
    fields = payload.model_dump(exclude_unset=True)
    if "display_name" in fields:
        current_user.display_name = fields["display_name"]
    if "avatar_url" in fields:
        current_user.avatar_url = fields["avatar_url"]
    if fields.get("daily_goal") is not None:
        current_user.daily_goal = fields["daily_goal"]
    db.commit()
    db.refresh(current_user)
    return _as_auth_user(current_user, readonly=False)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(payload: PasswordChange, current_user: Writer, db: DbSession):
    if current_user.password_hash is None or not verify_password(
        payload.current_password, current_user.password_hash
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Senha atual incorreta.")
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
