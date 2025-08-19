import logging
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from .config_provider import ConfigProvider


class AzureStorageConfigProvider(ConfigProvider):
    """
    Provides configuration from a file stored in Azure Storage.
    Returns the file content as a raw string.
    """

    def __init__(
        self, account_url: str, container_name: str, blob_name: str, credential: Optional[DefaultAzureCredential] = None
    ):
        """
        Initialize Azure Storage config provider

        Args:
            account_url: The Azure Storage account URL
            container_name: The container name
            blob_name: The blob name
            credential: Azure credential for authentication
        """
        self.account_url = account_url
        self.container_name = container_name
        self.blob_name = blob_name
        self.credential = credential or DefaultAzureCredential()
        self.client = BlobServiceClient(account_url=account_url, credential=self.credential)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_config(self) -> str | None:
        """
        Fetches the raw config data from a file in Azure Storage.
        """
        try:
            container_client = self.client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(self.blob_name)

            # Check if blob exists
            if not blob_client.exists():
                self.logger.error(
                    f"Blob '{self.blob_name}' does not exist in container '{self.container_name}' in storage account."
                )
                return None

            blob_data = blob_client.download_blob()
            data = blob_data.readall().decode("utf-8")

            self.logger.info(f"Successfully fetched config file from Azure Storage: {self.container_name}/{self.blob_name}")
            return data
        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred while fetching config from Azure Storage: {self.container_name}/{self.blob_name}: {e}"
            )
            return None
