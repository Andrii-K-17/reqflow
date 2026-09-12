import uuid
from datetime import UTC, datetime, timedelta
from typing import Literal

import bcrypt
from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()

TokenType = Literal["access", "refresh"]


class InvalidTokenError(Exception):
    pass


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except ValueError, TypeError:
        return False


def create_token(user_id: uuid.UUID, token_type: TokenType) -> str:
    expires_delta = (
        timedelta(minutes=settings.access_token_expire_minutes)
        if token_type == "access"
        else timedelta(days=settings.refresh_token_expire_days)
    )
    expire = datetime.now(UTC) + expires_delta
    payload = {"sub": str(user_id), "type": token_type, "exp": expire}

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str, expected_type: TokenType) -> uuid.UUID:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise InvalidTokenError("Token is invalid or expired") from exc

    if payload.get("type") != expected_type:
        raise InvalidTokenError(f"Expected {expected_type} token")

    sub = payload.get("sub")
    if sub is None:
        raise InvalidTokenError("Token missing subject")

    return uuid.UUID(sub)
