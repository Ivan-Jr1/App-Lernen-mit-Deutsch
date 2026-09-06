"""Dependências compartilhadas pelos routers.

Sem autenticação real nesta versão: são dois usuários fixos e o cliente diz
quem está agindo via `?user=ivan` ou o header `X-User`. Trocar isto por JWT é
um passo isolado descrito no README.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    user: Annotated[str | None, Query(description="username de quem está agindo")] = None,
    x_user: Annotated[str | None, Header()] = None,
) -> User:
    username = user or x_user
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe o usuário via ?user= ou o header X-User.",
        )

    found = db.scalar(select(User).where(User.username == username))
    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário '{username}' não existe.",
        )
    return found


CurrentUser = Annotated[User, Depends(get_current_user)]
