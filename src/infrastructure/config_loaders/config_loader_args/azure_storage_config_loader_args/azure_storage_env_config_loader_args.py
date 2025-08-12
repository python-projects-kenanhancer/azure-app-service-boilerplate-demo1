from dataclasses import dataclass
from typing import Optional

from azure.identity import DefaultAzureCredential

from ..config_loader_args import ConfigLoaderArgs


@dataclass
class AzureStorageEnvConfigLoaderArgs(ConfigLoaderArgs):
    """Azure Storage environment configuration loader arguments"""

    account_url_env_var: str = "AZURE_STORAGE_ACCOUNT_URL"
    blob_path_env_var: str = "AZURE_STORAGE_BLOB_PATH"
    credential: Optional[DefaultAzureCredential] = None

    def __post_init__(self):
        """Validate required environment variables"""
        import os

        if not os.getenv(self.account_url_env_var):
            raise ValueError(f"Environment variable '{self.account_url_env_var}' is required")
        if not os.getenv(self.blob_path_env_var):
            raise ValueError(f"Environment variable '{self.blob_path_env_var}' is required")
