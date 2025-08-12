from typing import Type

from ...config_loader_args import GcpStorageEnvConfigLoaderArgs
from ...config_loader_factory import ConfigLoaderFactory
from ..base_inject_settings import TSettings, inject_settings


def load_settings_from_gcp_storage_env(
    *, bucket_name: str, blob_name: str, project_id: str, SettingsClass: Type[TSettings]
) -> TSettings:
    gcp_env_config_loader = ConfigLoaderFactory.get_loader(
        GcpStorageEnvConfigLoaderArgs(bucket_name=bucket_name, blob_name=blob_name, project_id=project_id)
    )
    raw_config = gcp_env_config_loader.load()
    return SettingsClass(**raw_config)


def inject_settings_from_gcp_storage_env(bucket_name: str, blob_name: str, project_id: str, param_name: str = "settings"):
    return inject_settings(
        load_settings_from_gcp_storage_env,
        param_name=param_name,
        bucket_name=bucket_name,
        blob_name=blob_name,
        project_id=project_id,
    )
