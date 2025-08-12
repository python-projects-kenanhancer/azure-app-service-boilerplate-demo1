from .config_loader_args import ConfigLoaderArgs


class EnvConfigLoaderArgs(ConfigLoaderArgs):
    def __init__(self, file_path: str):
        self.file_path = file_path
