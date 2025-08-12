from dataclasses import dataclass
from typing import Optional

from azure.identity import DefaultAzureCredential

from ..config_loader_args import ConfigLoaderArgs


@dataclass
class AzureKeyVaultEnvConfigLoaderArgs(ConfigLoaderArgs):
    """Azure Key Vault environment configuration loader arguments"""

    vault_url_env_var: str = "AZURE_KEYVAULT_URL"
    secret_name_env_var: str = "AZURE_KEYVAULT_SECRET_NAME"
    credential: Optional[DefaultAzureCredential] = None

    def __post_init__(self):
        """Validate required environment variables"""
        import os

        if not os.getenv(self.vault_url_env_var):
            raise ValueError(f"Environment variable '{self.vault_url_env_var}' is required")
        if not os.getenv(self.secret_name_env_var):
            raise ValueError(f"Environment variable '{self.secret_name_env_var}' is required")
