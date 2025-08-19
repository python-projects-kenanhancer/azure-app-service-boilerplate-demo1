from typing import overload

from .config_loader import ConfigLoader
from .config_loader_args import (
    AzureKeyVaultEnvConfigLoaderArgs,
    AzureStorageEnvConfigLoaderArgs,
    ConfigLoaderArgs,
    EnvConfigLoaderArgs,
    GcpSecretEnvConfigLoaderArgs,
    GcpSecretJsonConfigLoaderArgs,
    GcpSecretYamlConfigLoaderArgs,
    GcpStorageEnvConfigLoaderArgs,
    GcpStorageJsonConfigLoaderArgs,
    GcpStorageYamlConfigLoaderArgs,
    JsonConfigLoaderArgs,
    YamlConfigLoaderArgs,
)
from .config_providers import (
    AzureKeyVaultConfigProvider,
    AzureStorageConfigProvider,
    FileConfigProvider,
    GcpSecretConfigProvider,
    GcpStorageConfigProvider,
)
from .env_config_loader import EnvConfigLoader
from .env_config_processors import DefaultEnvConfigProcessor
from .json_config_loader import JsonConfigLoader
from .yaml_config_loader import YamlConfigLoader


class ConfigLoaderFactory:
    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpSecretEnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpSecretJsonConfigLoaderArgs) -> JsonConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpSecretYamlConfigLoaderArgs) -> YamlConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpStorageEnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpStorageJsonConfigLoaderArgs) -> JsonConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: GcpStorageYamlConfigLoaderArgs) -> YamlConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: AzureKeyVaultEnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: AzureStorageEnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: EnvConfigLoaderArgs) -> EnvConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: JsonConfigLoaderArgs) -> JsonConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: YamlConfigLoaderArgs) -> YamlConfigLoader: ...

    @overload
    @staticmethod
    def get_loader(config_loader_args: ConfigLoaderArgs) -> ConfigLoader: ...

    @staticmethod
    def _create_gcp_secret_env_loader(config_loader_args: GcpSecretEnvConfigLoaderArgs) -> EnvConfigLoader:
        """Create GCP Secret environment config loader."""
        config_provider = GcpSecretConfigProvider(
            secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
        )
        env_processor = DefaultEnvConfigProcessor()
        return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)

    @staticmethod
    def _create_gcp_secret_json_loader(config_loader_args: GcpSecretJsonConfigLoaderArgs) -> JsonConfigLoader:
        """Create GCP Secret JSON config loader."""
        config_provider = GcpSecretConfigProvider(
            secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
        )
        return JsonConfigLoader(config_provider=config_provider)

    @staticmethod
    def _create_gcp_secret_yaml_loader(config_loader_args: GcpSecretYamlConfigLoaderArgs) -> YamlConfigLoader:
        """Create GCP Secret YAML config loader."""
        config_provider = GcpSecretConfigProvider(
            secret_name=config_loader_args.secret_name, project_id=config_loader_args.project_id
        )
        return YamlConfigLoader(config_provider=config_provider)

    @staticmethod
    def _create_gcp_storage_env_loader(config_loader_args: GcpStorageEnvConfigLoaderArgs) -> EnvConfigLoader:
        """Create GCP Storage environment config loader."""
        config_provider = GcpStorageConfigProvider(
            bucket_name=config_loader_args.bucket_name,
            blob_name=config_loader_args.blob_name,
            project_id=config_loader_args.project_id,
        )
        env_processor = DefaultEnvConfigProcessor()
        return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)

    @staticmethod
    def _create_gcp_storage_json_loader(config_loader_args: GcpStorageJsonConfigLoaderArgs) -> JsonConfigLoader:
        """Create GCP Storage JSON config loader."""
        config_provider = GcpStorageConfigProvider(
            bucket_name=config_loader_args.bucket_name,
            blob_name=config_loader_args.blob_name,
            project_id=config_loader_args.project_id,
        )
        return JsonConfigLoader(config_provider=config_provider)

    @staticmethod
    def _create_gcp_storage_yaml_loader(config_loader_args: GcpStorageYamlConfigLoaderArgs) -> YamlConfigLoader:
        """Create GCP Storage YAML config loader."""
        config_provider = GcpStorageConfigProvider(
            bucket_name=config_loader_args.bucket_name,
            blob_name=config_loader_args.blob_name,
            project_id=config_loader_args.project_id,
        )
        return YamlConfigLoader(config_provider=config_provider)

    @staticmethod
    def _create_azure_keyvault_env_loader(config_loader_args: AzureKeyVaultEnvConfigLoaderArgs) -> EnvConfigLoader:
        """Create Azure KeyVault environment config loader."""
        import os

        vault_url = os.getenv(config_loader_args.vault_url_env_var)
        secret_name = os.getenv(config_loader_args.secret_name_env_var)
        if not vault_url:
            raise ValueError(f"Environment variable {config_loader_args.vault_url_env_var} not set")
        if not secret_name:
            raise ValueError(f"Environment variable {config_loader_args.secret_name_env_var} not set")
        config_provider = AzureKeyVaultConfigProvider(
            vault_url=vault_url, secret_name=secret_name, credential=config_loader_args.credential
        )
        env_processor = DefaultEnvConfigProcessor()
        return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)

    @staticmethod
    def _create_azure_storage_env_loader(config_loader_args: AzureStorageEnvConfigLoaderArgs) -> EnvConfigLoader:
        """Create Azure Storage environment config loader."""
        import os

        account_url = os.getenv(config_loader_args.account_url_env_var)
        blob_path = os.getenv(config_loader_args.blob_path_env_var)
        if not account_url:
            raise ValueError(f"Environment variable {config_loader_args.account_url_env_var} not set")
        if not blob_path:
            raise ValueError(f"Environment variable {config_loader_args.blob_path_env_var} not set")

        # Parse container and blob name from blob_path (format: "container_name/blob_name")
        if "/" not in blob_path:
            raise ValueError(f"blob_path must be in format 'container_name/blob_name', got: {blob_path}")
        container_name, blob_name = blob_path.split("/", 1)

        config_provider = AzureStorageConfigProvider(
            account_url=account_url, container_name=container_name, blob_name=blob_name, credential=config_loader_args.credential
        )
        env_processor = DefaultEnvConfigProcessor()
        return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)

    @staticmethod
    def _create_file_env_loader(config_loader_args: EnvConfigLoaderArgs) -> EnvConfigLoader:
        """Create file-based environment config loader."""
        config_provider = FileConfigProvider(file_path=config_loader_args.file_path)
        env_processor = DefaultEnvConfigProcessor()
        return EnvConfigLoader(config_provider=config_provider, env_processor=env_processor)

    @staticmethod
    def _create_file_json_loader(config_loader_args: JsonConfigLoaderArgs) -> JsonConfigLoader:
        """Create file-based JSON config loader."""
        config_provider = FileConfigProvider(file_path=config_loader_args.file_path)
        return JsonConfigLoader(config_provider=config_provider)

    @staticmethod
    def _create_file_yaml_loader(config_loader_args: YamlConfigLoaderArgs) -> YamlConfigLoader:
        """Create file-based YAML config loader."""
        config_provider = FileConfigProvider(file_path=config_loader_args.file_path)
        return YamlConfigLoader(config_provider=config_provider)

    @staticmethod
    def get_loader(config_loader_args: ConfigLoaderArgs) -> ConfigLoader:
        """Get the appropriate config loader based on the provided arguments."""
        # Create a mapping of argument types to their corresponding loader creation methods
        loader_mapping = {
            GcpSecretEnvConfigLoaderArgs: ConfigLoaderFactory._create_gcp_secret_env_loader,
            GcpSecretJsonConfigLoaderArgs: ConfigLoaderFactory._create_gcp_secret_json_loader,
            GcpSecretYamlConfigLoaderArgs: ConfigLoaderFactory._create_gcp_secret_yaml_loader,
            GcpStorageEnvConfigLoaderArgs: ConfigLoaderFactory._create_gcp_storage_env_loader,
            GcpStorageJsonConfigLoaderArgs: ConfigLoaderFactory._create_gcp_storage_json_loader,
            GcpStorageYamlConfigLoaderArgs: ConfigLoaderFactory._create_gcp_storage_yaml_loader,
            AzureKeyVaultEnvConfigLoaderArgs: ConfigLoaderFactory._create_azure_keyvault_env_loader,
            AzureStorageEnvConfigLoaderArgs: ConfigLoaderFactory._create_azure_storage_env_loader,
            EnvConfigLoaderArgs: ConfigLoaderFactory._create_file_env_loader,
            JsonConfigLoaderArgs: ConfigLoaderFactory._create_file_json_loader,
            YamlConfigLoaderArgs: ConfigLoaderFactory._create_file_yaml_loader,
        }

        # Find the appropriate loader creation method
        for arg_type, loader_method in loader_mapping.items():
            if isinstance(config_loader_args, arg_type):
                return loader_method(config_loader_args)

        # If no matching type found, raise an error
        raise ValueError(f"Unsupported loader arguments: {config_loader_args}")
