from ..config_loader_args import ConfigLoaderArgs


class GcpSecretJsonConfigLoaderArgs(ConfigLoaderArgs):
    def __init__(self, secret_name: str, project_id: str):
        self.secret_name = secret_name
        self.project_id = project_id
