"""Dependências compartilhadas pelos routers: sessão, usuário autenticado e a
exigência de permissão de escrita.

Autenticação por token JWT no header `Authorization: Bearer <token>`. O token de
visitante carrega `readonly=True` e só passa nos endpoints de leitura.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth import decode_access_token
from app.database import get_db
from app.models import User

DbSession = Annotated[Session, Depends(get_db)]

_bearer = HTTPBearer(auto_error=False)


def _authenticate(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> tuple[User, bool]:
    """Valida o token e devolve (usuário, é_somente_leitura)."""
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Faça login para continuar.")

    token = decode_access_token(credentials.credentials)
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão inválida ou expirada.")

    user = db.get(User, token.user_id)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Conta não encontrada.")

    return user, token.readonly


def get_current_user(auth: Annotated[tuple[User, bool], Depends(_authenticate)]) -> User:
    """Qualquer sessão válida, inclusive a de visitante (somente leitura)."""
    return auth[0]


def require_writer(auth: Annotated[tuple[User, bool], Depends(_authenticate)]) -> User:
    """Bloqueia a sessão de visitante."""
    user, readonly = auth
    if readonly:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Acesso de visitante é somente leitura. Faça login para alterar dados.",
        )
    return user


Reader = Annotated[User, Depends(get_current_user)]  # leitura: inclui visitante
Writer = Annotated[User, Depends(require_writer)]  # escrita: bloqueia visitante
