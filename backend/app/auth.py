"""Hash de senha (argon2) e emissão/validação de tokens JWT.

Isolado dos routers para ser testável e para concentrar as decisões de segurança
num lugar só.
"""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings

_password_hasher = PasswordHash.recommended()
_ALGORITHM = "HS256"


def hash_password(plain: str) -> str:
    return _password_hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _password_hasher.verify(plain, hashed)


def create_access_token(user_id: int, username: str, *, readonly: bool = False) -> str:
    """Token de sessão. `readonly` marca o acesso de visitante."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "username": username,
        "readonly": readonly,
        "iat": now,
        "exp": now + timedelta(days=settings.jwt_expire_days),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALGORITHM)


class TokenData:
    """Conteúdo já validado de um token."""

    def __init__(self, user_id: int, username: str, readonly: bool) -> None:
        self.user_id = user_id
        self.username = username
        self.readonly = readonly


def decode_access_token(token: str) -> TokenData | None:
    """Devolve os dados do token ou None se for inválido/expirado."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[_ALGORITHM])
        return TokenData(
            user_id=int(payload["sub"]),
            username=payload["username"],
            readonly=bool(payload.get("readonly", False)),
        )
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
