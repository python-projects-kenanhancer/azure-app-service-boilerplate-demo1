import os
from functools import wraps
from typing import Any, Callable, Dict, Type

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from ...config_providers import AzureKeyVaultConfigProvider


def inject_settings_from_azure_keyvault_env(
    vault_url_env_var: str = "AZURE_KEYVAULT_URL",
    secret_name_env_var: str = "AZURE_KEYVAULT_SECRET_NAME",
    credential: DefaultAzureCredential = None,
) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorator to inject settings from Azure Key Vault using environment variables

    Args:
        vault_url_env_var: Environment variable name for the Key Vault URL
        secret_name_env_var: Environment variable name for the secret name
        credential: Azure credential for authentication

    Returns:
        Decorated class with injected settings
    """

    def decorator(cls: Type[Any]) -> Type[Any]:
        @wraps(cls)
        def wrapper(*args, **kwargs):
            # Get configuration from environment variables
            vault_url = os.getenv(vault_url_env_var)
            secret_name = os.getenv(secret_name_env_var)

            if not vault_url:
                raise ValueError(f"Environment variable '{vault_url_env_var}' is required")
            if not secret_name:
                raise ValueError(f"Environment variable '{secret_name_env_var}' is required")

            # Create Azure Key Vault provider
            provider = AzureKeyVaultConfigProvider(vault_url, credential)

            # Load configuration
            config = provider.load_config(secret_name)

            # Inject configuration into the class
            for key, value in config.items():
                setattr(cls, key, value)

            return cls(*args, **kwargs)

        return wrapper

    return decorator
