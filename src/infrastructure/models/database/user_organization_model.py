"""User-Organization relationship model for database."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import Base


class UserOrganization(Base):
    """User-Organization relationship model."""

    __tablename__ = "user_organizations"

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Role and permissions
    role = Column(String(50), default="member", nullable=False)  # owner, admin, member
    permissions = Column(String(500), nullable=True)  # JSON string of permissions

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_organizations")
    organization = relationship("Organization", back_populates="user_organizations")

    def __repr__(self) -> str:
        return f"<UserOrganization(user_id={self.user_id}, org_id={self.organization_id}, role='{self.role}')>"
