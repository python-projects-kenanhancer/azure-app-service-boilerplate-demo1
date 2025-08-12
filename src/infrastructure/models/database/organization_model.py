"""Organization model for database."""

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.orm import relationship

from .base_model import Base


class Organization(Base):
    """Organization model representing user organizations."""

    __tablename__ = "organizations"

    # Organization identification
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)

    # Organization details
    description = Column(Text, nullable=True)
    website_url = Column(String(255), nullable=True)
    logo_url = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)

    # Relationships
    user_organizations = relationship("UserOrganization", back_populates="organization")

    def __repr__(self) -> str:
        return f"<Organization(name='{self.name}', slug='{self.slug}')>"
