from ..config_loader_args import ConfigLoaderArgs


class GcpStorageJsonConfigLoaderArgs(ConfigLoaderArgs):
    def __init__(self, bucket_name: str, blob_name: str, project_id: str):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.project_id = project_id
