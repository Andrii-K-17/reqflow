from app.core.security import (
    InvalidTokenError,
    create_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenPair


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._users = user_repository

    async def register(self, *, email: str, password: str, full_name: str) -> User:
        if await self._users.get_by_email(email) is not None:
            raise EmailAlreadyRegisteredError(f"Email {email} is already registered")
        return await self._users.create(
            email=email, hashed_password=hash_password(password), full_name=full_name
        )

    async def authenticate(self, *, email: str, password: str) -> User:
        user = await self._users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        return user

    def issue_tokens(self, user: User) -> TokenPair:
        return TokenPair(
            access_token=create_token(user.id, "access"),
            refresh_token=create_token(user.id, "refresh"),
        )

    async def refresh(self, refresh_token: str) -> TokenPair:
        try:
            user_id = decode_token(refresh_token, "refresh")
        except InvalidTokenError as exc:
            raise InvalidCredentialsError("Invalid refresh token") from exc

        user = await self._users.get_by_id(user_id)
        if user is None:
            raise InvalidCredentialsError("User no longer exists")

        return self.issue_tokens(user)
