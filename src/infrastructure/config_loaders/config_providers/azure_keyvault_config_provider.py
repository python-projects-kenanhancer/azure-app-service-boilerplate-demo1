from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from .config_provider import ConfigProvider


class AzureKeyVaultConfigProvider(ConfigProvider):
    """Azure Key Vault configuration provider"""

    def __init__(self, vault_url: str, credential: Optional[DefaultAzureCredential] = None):
        """
        Initialize Azure Key Vault config provider

        Args:
            vault_url: The URL of the Azure Key Vault
            credential: Azure credential for authentication
        """
        self.vault_url = vault_url
        self.credential = credential or DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=self.credential)

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from Azure Key Vault

        Args:
            config_path: The secret name in Key Vault

        Returns:
            Dictionary containing the configuration
        """
        try:
            secret = self.client.get_secret(config_path)
            # Assuming the secret value is JSON or can be parsed as key-value pairs
            import json

            return json.loads(secret.value)
        except Exception as e:
            raise ValueError(f"Failed to load config from Azure Key Vault: {e}")

    def get_secret(self, secret_name: str) -> str:
        """
        Get a specific secret from Azure Key Vault

        Args:
            secret_name: The name of the secret

        Returns:
            The secret value
        """
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            raise ValueError(f"Failed to get secret '{secret_name}' from Azure Key Vault: {e}")
