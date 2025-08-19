import os
from functools import wraps
from typing import Any, Callable, Type

from azure.identity import DefaultAzureCredential

from ...config_providers import AzureStorageConfigProvider


def inject_settings_from_azure_storage_env(
    account_url_env_var: str = "AZURE_STORAGE_ACCOUNT_URL",
    blob_path_env_var: str = "AZURE_STORAGE_BLOB_PATH",
    credential: DefaultAzureCredential = None,
) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorator to inject settings from Azure Storage using environment variables

    Args:
        account_url_env_var: Environment variable name for the Storage account URL
        blob_path_env_var: Environment variable name for the blob path (container/blob)
        credential: Azure credential for authentication

    Returns:
        Decorated class with injected settings
    """

    def decorator(cls: Type[Any]) -> Type[Any]:
        @wraps(cls)
        def wrapper(*args, **kwargs):
            # Get configuration from environment variables
            account_url = os.getenv(account_url_env_var)
            blob_path = os.getenv(blob_path_env_var)

            if not account_url:
                raise ValueError(f"Environment variable '{account_url_env_var}' is required")
            if not blob_path:
                raise ValueError(f"Environment variable '{blob_path_env_var}' is required")

            # Create Azure Storage provider
            provider = AzureStorageConfigProvider(account_url, credential)

            # Load configuration
            config = provider.load_config(blob_path)

            # Inject configuration into the class
            for key, value in config.items():
                setattr(cls, key, value)

            return cls(*args, **kwargs)

        return wrapper

    return decorator
