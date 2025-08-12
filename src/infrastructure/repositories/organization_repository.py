"""Organization repository for database operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.database.organization_model import Organization
from .base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    """Repository for Organization model operations."""

    def __init__(self, db_session: Session):
        super().__init__(Organization, db_session)

    def get_by_slug(self, slug: str) -> Optional[Organization]:
        """Get organization by slug."""
        return self.filter_one(slug=slug)

    def get_active_organizations(self) -> List[Organization]:
        """Get all active organizations."""
        return self.filter_by(is_active=True)

    def get_public_organizations(self) -> List[Organization]:
        """Get all public organizations."""
        return self.filter_by(is_public=True, is_active=True)

    def create_organization(self, name: str, slug: str, description: Optional[str] = None) -> Organization:
        """Create a new organization."""
        return self.create(name=name, slug=slug, description=description, is_active=True, is_public=False)

    def update_organization(self, org_id: int, **kwargs) -> Optional[Organization]:
        """Update organization information."""
        return self.update(org_id, **kwargs)

    def deactivate_organization(self, org_id: int) -> Optional[Organization]:
        """Deactivate an organization."""
        return self.update(org_id, is_active=False)

    def make_public(self, org_id: int) -> Optional[Organization]:
        """Make organization public."""
        return self.update(org_id, is_public=True)

    def make_private(self, org_id: int) -> Optional[Organization]:
        """Make organization private."""
        return self.update(org_id, is_public=False)
