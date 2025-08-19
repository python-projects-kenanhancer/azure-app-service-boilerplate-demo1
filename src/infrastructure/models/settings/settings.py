from pydantic import BaseModel, ConfigDict

from domain import GreetingLanguage, GreetingType

from . import Environment


class Settings(BaseModel):
    project_env: Environment
    default_name: str
    greeting_type: GreetingType
    greeting_language: GreetingLanguage
    web_framework: str
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    logger_name: str = "azure_app_service"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "azure_app_service_db"
    db_user: str = "app_user"
    db_password: str = "app_password"
    jwt_secret: str = "your-super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        # The typed decorator will call this to serialize the response
        return self.model_dump()
