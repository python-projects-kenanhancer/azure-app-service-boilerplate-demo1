from unittest.mock import Mock, patch

import pytest

from infrastructure import AzureKeyVaultConfigProvider, AzureStorageConfigProvider


class TestAzureKeyVaultConfigProvider:
    """Test Azure Key Vault configuration provider"""

    @patch("infrastructure.config_loaders.config_providers.azure_keyvault_config_provider.SecretClient")
    @patch("infrastructure.config_loaders.config_providers.azure_keyvault_config_provider.DefaultAzureCredential")
    def test_load_config_success(self, mock_credential, mock_client_class):
        """Test successful configuration loading from Azure Key Vault"""
        # Mock the secret client
        mock_client = Mock()
        mock_client.get_secret.return_value.value = '{"key1": "value1", "key2": "value2"}'
        mock_client_class.return_value = mock_client

        # Create provider
        provider = AzureKeyVaultConfigProvider("https://test.vault.azure.net/")

        # Test loading config
        result = provider.load_config("test-secret")

        assert result == {"key1": "value1", "key2": "value2"}
        mock_client.get_secret.assert_called_once_with("test-secret")

    @patch("infrastructure.config_loaders.config_providers.azure_keyvault_config_provider.SecretClient")
    @patch("infrastructure.config_loaders.config_providers.azure_keyvault_config_provider.DefaultAzureCredential")
    def test_get_secret_success(self, mock_credential, mock_client_class):
        """Test successful secret retrieval from Azure Key Vault"""
        # Mock the secret client
        mock_client = Mock()
        mock_client.get_secret.return_value.value = "secret-value"
        mock_client_class.return_value = mock_client

        # Create provider
        provider = AzureKeyVaultConfigProvider("https://test.vault.azure.net/")

        # Test getting secret
        result = provider.get_secret("test-secret")

        assert result == "secret-value"
        mock_client.get_secret.assert_called_once_with("test-secret")


class TestAzureStorageConfigProvider:
    """Test Azure Storage configuration provider"""

    @patch("infrastructure.config_loaders.config_providers.azure_storage_config_provider.BlobServiceClient")
    @patch("infrastructure.config_loaders.config_providers.azure_storage_config_provider.DefaultAzureCredential")
    def test_load_config_json_success(self, mock_credential, mock_client_class):
        """Test successful JSON configuration loading from Azure Storage"""
        # Mock the blob client
        mock_container_client = Mock()
        mock_blob_client = Mock()
        mock_blob_data = Mock()
        mock_blob_data.readall.return_value = b'{"key1": "value1", "key2": "value2"}'
        mock_blob_client.download_blob.return_value = mock_blob_data

        mock_container_client.get_blob_client.return_value = mock_blob_client
        mock_client = Mock()
        mock_client.get_container_client.return_value = mock_container_client
        mock_client_class.return_value = mock_client

        # Create provider
        provider = AzureStorageConfigProvider("https://test.blob.core.windows.net/")

        # Test loading config
        result = provider.load_config("container/config.json")

        assert result == {"key1": "value1", "key2": "value2"}
        mock_container_client.get_blob_client.assert_called_once_with("config.json")

    @patch("infrastructure.config_loaders.config_providers.azure_storage_config_provider.BlobServiceClient")
    @patch("infrastructure.config_loaders.config_providers.azure_storage_config_provider.DefaultAzureCredential")
    def test_get_blob_content_success(self, mock_credential, mock_client_class):
        """Test successful blob content retrieval from Azure Storage"""
        # Mock the blob client
        mock_container_client = Mock()
        mock_blob_client = Mock()
        mock_blob_data = Mock()
        mock_blob_data.readall.return_value = b"blob-content"
        mock_blob_client.download_blob.return_value = mock_blob_data

        mock_container_client.get_blob_client.return_value = mock_blob_client
        mock_client = Mock()
        mock_client.get_container_client.return_value = mock_container_client
        mock_client_class.return_value = mock_client

        # Create provider
        provider = AzureStorageConfigProvider("https://test.blob.core.windows.net/")

        # Test getting blob content
        result = provider.get_blob_content("container", "blob.txt")

        assert result == "blob-content"
        mock_container_client.get_blob_client.assert_called_once_with("blob.txt")
