"""SQLAlchemy module for dependency injection."""

from typing import Optional

from injector import Module, provider, singleton
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from ..logger import LoggerStrategy
from ..models.settings import Settings


class SQLAlchemyModule(Module):
    """Module for SQLAlchemy database dependency injection."""

    @singleton
    @provider
    def provide_database_engine(self, settings: Settings, logger: LoggerStrategy) -> Optional[Engine]:
        """Provide SQLAlchemy database engine."""
        try:
            # In a real application, these would come from settings
            db_host = settings.db_host
            db_port = settings.db_port
            db_name = settings.db_name
            db_user = settings.db_user
            db_password = settings.db_password

            # Build database URL
            if db_password:
                database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            else:
                database_url = f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"

            logger.info(f"Database connecting to {db_host}:{db_port}/{db_name}")

            # Create engine with appropriate configuration
            engine = create_engine(
                database_url,
                echo=settings.debug,  # Log SQL queries in debug mode
                poolclass=StaticPool,  # Use static pool for development
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=3600,  # Recycle connections every hour
            )

            # Test connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logger.info(f"Database connected successfully to {db_host}:{db_port}/{db_name}")
            return engine

        except Exception as e:
            logger.warning(f"Failed to connect to database: {str(e)}")
            logger.info("Application will run without database (using in-memory SQLite)")

            # Fallback to in-memory SQLite for development
            fallback_url = "sqlite:///:memory:"
            fallback_engine = create_engine(fallback_url, echo=settings.debug, connect_args={"check_same_thread": False})

            logger.info("Using in-memory SQLite database")
            return fallback_engine

    @provider
    def provide_database_session_factory(self, engine) -> sessionmaker:
        """Provide SQLAlchemy session factory."""
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @provider
    def provide_database_session(self, session_factory: sessionmaker) -> Session:
        """Provide SQLAlchemy database session."""
        return session_factory()
