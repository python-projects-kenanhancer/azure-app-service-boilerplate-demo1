from pathlib import Path
from typing import Optional

from ...config_loaders import ConfigLoaderFactory, YamlConfigLoaderArgs
from .settings import Settings


def load_settings_from_development_yml(file_path: str = "development.yml") -> Settings:
    """
    Load settings from the development.yml file.

    Args:
        file_path: Path to the development.yml file (default: "development.yml")

    Returns:
        Settings instance populated with configuration from the YAML file

    Raises:
        FileNotFoundError: If the development.yml file doesn't exist
        ValueError: If the YAML content is invalid
        Exception: For other configuration loading errors
    """
    # Check if file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Development configuration file not found: {file_path}")

    # Use the existing YAML config loader infrastructure
    yaml_config_loader = ConfigLoaderFactory.get_loader(YamlConfigLoaderArgs(file_path=file_path))

    # Load the raw configuration
    raw_config = yaml_config_loader.load()

    # Create Settings instance with the loaded configuration
    return Settings(**raw_config)


def load_settings_with_fallback(primary_file: str = "development.yml", fallback_file: Optional[str] = None) -> Settings:
    """
    Load settings with fallback support.

    Args:
        primary_file: Primary configuration file to load (default: "development.yml")
        fallback_file: Fallback configuration file if primary doesn't exist

    Returns:
        Settings instance populated with configuration

    Raises:
        FileNotFoundError: If neither file exists
        ValueError: If the YAML content is invalid
        Exception: For other configuration loading errors
    """
    try:
        return load_settings_from_development_yml(primary_file)
    except FileNotFoundError:
        if fallback_file and Path(fallback_file).exists():
            return load_settings_from_development_yml(fallback_file)
        elif fallback_file:
            raise FileNotFoundError(f"Neither {primary_file} nor {fallback_file} found")
        else:
            # Return default settings if no fallback specified
            return Settings()
    except Exception as e:
        # Re-raise other exceptions
        raise e
