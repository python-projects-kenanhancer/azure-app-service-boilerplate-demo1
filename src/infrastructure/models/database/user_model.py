"""User model for database."""

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.orm import relationship

from .base_model import Base


class User(Base):
    """User model representing application users."""

    __tablename__ = "users"

    # User identification
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)

    # User details
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # Authentication
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Additional info
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)

    # Relationships
    user_organizations = relationship("UserOrganization", back_populates="user")
    sessions = relationship("Session", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"
