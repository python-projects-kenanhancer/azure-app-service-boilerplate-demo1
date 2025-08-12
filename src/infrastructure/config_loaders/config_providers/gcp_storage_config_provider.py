import logging

from google.auth.exceptions import DefaultCredentialsError
from google.cloud.storage import Client as StorageClient

from .config_provider import ConfigProvider


class GcpStorageConfigProvider(ConfigProvider):
    """
    Provides configuration from a file stored in Google Cloud Storage.
    Returns the file content as a raw string.
    """

    def __init__(self, bucket_name: str, blob_name: str, project_id: str):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.project_id = project_id
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_config(self) -> str | None:
        """
        Fetches the raw config data from a file in a GCS bucket.
        """
        try:
            client = StorageClient(project=self.project_id)
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.blob_name)
            if not blob.exists():
                self.logger.error(
                    f"Blob '{self.blob_name}' does not exist in bucket '{self.bucket_name}' within project '{self.project_id}'."
                )
                return None

            data = blob.download_as_text()
            self.logger.info(
                f"Successfully fetched config file from GCS: gs://{self.bucket_name}/{self.blob_name} (Project: {self.project_id})"
            )
            return data
        except DefaultCredentialsError as e:
            self.logger.error(f"Error loading credentials for project '{self.project_id}': {e}")
            return None
        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred while fetching config from GCS: gs://{self.bucket_name}/{self.blob_name} (Project: {self.project_id}): {e}"
            )
            return None
