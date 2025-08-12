from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from .config_provider import ConfigProvider


class AzureStorageConfigProvider(ConfigProvider):
    """Azure Storage configuration provider"""

    def __init__(self, account_url: str, credential: Optional[DefaultAzureCredential] = None):
        """
        Initialize Azure Storage config provider
        
        Args:
            account_url: The Azure Storage account URL
            credential: Azure credential for authentication
        """
        self.account_url = account_url
        self.credential = credential or DefaultAzureCredential()
        self.client = BlobServiceClient(account_url=account_url, credential=self.credential)

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from Azure Storage Blob
        
        Args:
            config_path: The blob path in format "container_name/blob_name"
            
        Returns:
            Dictionary containing the configuration
        """
        try:
            # Parse container and blob name from config_path
            if '/' not in config_path:
                raise ValueError("config_path must be in format 'container_name/blob_name'")
            
            container_name, blob_name = config_path.split('/', 1)
            container_client = self.client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            
            # Download the blob content
            blob_data = blob_client.download_blob()
            content = blob_data.readall().decode('utf-8')
            
            # Parse content based on file extension
            if blob_name.endswith('.json'):
                import json
                return json.loads(content)
            elif blob_name.endswith('.yaml') or blob_name.endswith('.yml'):
                import yaml
                return yaml.safe_load(content)
            else:
                # Assume it's a simple key-value format
                config = {}
                for line in content.split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
                return config
                
        except Exception as e:
            raise ValueError(f"Failed to load config from Azure Storage: {e}")

    def get_blob_content(self, container_name: str, blob_name: str) -> str:
        """
        Get content from a specific blob
        
        Args:
            container_name: The container name
            blob_name: The blob name
            
        Returns:
            The blob content as string
        """
        try:
            container_client = self.client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob()
            return blob_data.readall().decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to get blob content '{container_name}/{blob_name}': {e}")
