from typing import Type

from ...config_loader_args import GcpSecretYamlConfigLoaderArgs
from ...config_loader_factory import ConfigLoaderFactory
from ..base_inject_settings import TSettings, inject_settings


def load_settings_from_gcp_secret_yaml(*, secret_name: str, project_id: str, SettingsClass: Type[TSettings]) -> TSettings:
    gcp_yaml_config_loader = ConfigLoaderFactory.get_loader(
        GcpSecretYamlConfigLoaderArgs(secret_name=secret_name, project_id=project_id)
    )
    raw_config = gcp_yaml_config_loader.load()
    return SettingsClass(**raw_config)


def inject_settings_from_gcp_secret_yaml(secret_name: str, project_id: str, param_name: str = "settings"):
    return inject_settings(
        load_settings_from_gcp_secret_yaml, param_name=param_name, secret_name=secret_name, project_id=project_id
    )
