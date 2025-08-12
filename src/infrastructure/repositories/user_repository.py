"""User repository for database operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.database.user_model import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""

    def __init__(self, db_session: Session):
        super().__init__(User, db_session)

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.filter_one(username=username)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.filter_one(email=email)

    def get_active_users(self) -> List[User]:
        """Get all active users."""
        return self.filter_by(is_active=True)

    def get_verified_users(self) -> List[User]:
        """Get all verified users."""
        return self.filter_by(is_verified=True)

    def authenticate_user(self, username: str, password_hash: str) -> Optional[User]:
        """Authenticate user with username and password hash."""
        return self.filter_one(username=username, password_hash=password_hash, is_active=True)

    def create_user(self, username: str, email: str, first_name: str, last_name: str, password_hash: str) -> User:
        """Create a new user."""
        return self.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
            is_active=True,
            is_verified=False,
        )

    def update_user_profile(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user profile information."""
        return self.update(user_id, **kwargs)

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user."""
        return self.update(user_id, is_active=False)

    def verify_user(self, user_id: int) -> Optional[User]:
        """Mark user as verified."""
        return self.update(user_id, is_verified=True)
