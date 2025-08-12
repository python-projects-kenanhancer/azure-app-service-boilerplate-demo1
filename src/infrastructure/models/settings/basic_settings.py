from pydantic_settings import BaseSettings

from .environment import Environment


class BasicSettings(BaseSettings):
    environment: Environment = Environment.DEV
    gcp_project_id: str = "default-project"
    app_config_bucket: str = "ovo-app-config"
    project_name: str = "ovo_gcp_cloud_function_ci_cd_demo"
