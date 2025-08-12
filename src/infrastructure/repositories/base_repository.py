"""Base repository for database operations."""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.database.base_model import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class providing common database operations."""

    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return self.db_session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = self.db_session.execute(stmt)
        return list(result.scalars().all())

    def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**kwargs)
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update a record by ID."""
        db_obj = self.get(id)
        if db_obj:
            for key, value in kwargs.items():
                setattr(db_obj, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        db_obj = self.get(id)
        if db_obj:
            self.db_session.delete(db_obj)
            self.db_session.commit()
            return True
        return False

    def filter_by(self, **kwargs) -> List[ModelType]:
        """Filter records by given criteria."""
        stmt = select(self.model).filter_by(**kwargs)
        result = self.db_session.execute(stmt)
        return list(result.scalars().all())

    def filter_one(self, **kwargs) -> Optional[ModelType]:
        """Get a single record by given criteria."""
        stmt = select(self.model).filter_by(**kwargs)
        result = self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    def exists(self, **kwargs) -> bool:
        """Check if a record exists with given criteria."""
        return self.filter_one(**kwargs) is not None

    def count(self, **kwargs) -> int:
        """Count records with given criteria."""
        stmt = select(self.model).filter_by(**kwargs)
        result = self.db_session.execute(stmt)
        return len(result.scalars().all())
