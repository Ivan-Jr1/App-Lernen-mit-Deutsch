"""Autenticação: contas fixas, definição de senha no primeiro acesso, login e
acesso de visitante (somente leitura).

Cadastro é fechado — só existem as contas criadas pelo seed.
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.auth import create_access_token, hash_password, verify_password
from app.deps import DbSession, Reader
from app.models import User
from app.schemas import AccountOut, AuthUser, Credentials, TokenOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _token_response(user: User, *, readonly: bool) -> TokenOut:
    return TokenOut(
        access_token=create_access_token(user.id, user.username, readonly=readonly),
        user=AuthUser(username=user.username, display_name=user.display_name, readonly=readonly),
    )


@router.get("/accounts", response_model=list[AccountOut])
def list_accounts(db: DbSession):
    """Contas disponíveis para login, e se cada uma já definiu senha."""
    accounts = db.scalars(
        select(User).where(User.is_guest.is_(False)).order_by(User.id)
    )
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
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Esta conta já tem senha. Faça login."
        )

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
    # readonly não fica no User; o endpoint /me serve só para o front confirmar a
    # sessão, então devolvemos o flag a partir do próprio usuário (visitante).
    return AuthUser(
        username=current_user.username,
        display_name=current_user.display_name,
        readonly=current_user.is_guest,
    )
