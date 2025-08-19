#!/usr/bin/env python3
"""
Example script demonstrating how to use the refactored settings with development.yml
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from infrastructure.models.settings import Settings, load_settings_from_development_yml, load_settings_with_fallback


def _display_llm_config(settings):
    """Display LLM configuration details."""
    if not settings.llm:
        return

    print(f"   - LLM default provider: {settings.llm.default_provider}")
    openai_config = settings.get_llm_provider("openai")
    if openai_config:
        print(f"   - OpenAI model: {openai_config.model}")
        print(f"   - OpenAI temperature: {openai_config.temperature}")


def _display_embedding_config(settings):
    """Display embedding configuration details."""
    if not settings.embedding:
        return

    print(f"   - Embedding default provider: {settings.embedding.default_provider}")
    openai_embedding = settings.get_embedding_provider("openai")
    if openai_embedding:
        print(f"   - OpenAI embedding model: {openai_embedding.model}")
        print(f"   - OpenAI embedding dimensions: {openai_embedding.dimensions}")


def _display_database_config(settings):
    """Display database configuration details."""
    if not settings.database:
        return

    print(f"   - Database default provider: {settings.database.default_provider}")
    postgres_config = settings.get_database_provider("postgres")
    if postgres_config:
        print(f"   - PostgreSQL host: {postgres_config.host}")
        print(f"   - PostgreSQL port: {postgres_config.port}")
        print(f"   - PostgreSQL database: {postgres_config.database}")


def _display_tools_config(settings):
    """Display tools configuration details."""
    if not settings.tools:
        return

    classifier_config = settings.get_tool_config("classifier")
    if classifier_config:
        print(f"   - Classifier LLM provider: {classifier_config.llm_provider}")


def _display_agents_config(settings):
    """Display agents configuration details."""
    if not settings.agents:
        return

    rag_agent_config = settings.get_agent_config("rag_agent")
    if rag_agent_config:
        print(f"   - RAG Agent QA assurance: {rag_agent_config.qa_assurance}")
        if rag_agent_config.qa_agent:
            print(f"   - QA Agent threshold: {rag_agent_config.qa_agent.threshold}")


def _demonstrate_development_yml_loading():
    """Demonstrate loading settings from development.yml."""
    print("1. Loading settings from development.yml:")
    try:
        settings = load_settings_from_development_yml("development.yml")
        print("   ✅ Successfully loaded settings")
        print(f"   - Project environment: {settings.project_env}")
        print(f"   - Default name: {settings.default_name}")
        print(f"   - Web framework: {settings.web_framework}")

        # Display various configuration sections
        _display_llm_config(settings)
        _display_embedding_config(settings)
        _display_database_config(settings)
        _display_tools_config(settings)
        _display_agents_config(settings)

    except FileNotFoundError:
        print("   ❌ development.yml file not found")
    except Exception as e:
        print(f"   ❌ Error loading settings: {e}")


def _demonstrate_fallback_loading():
    """Demonstrate loading settings with fallback."""
    print("2. Loading settings with fallback:")
    try:
        settings = load_settings_with_fallback(primary_file="development.yml", fallback_file="config.json")
        print("   ✅ Successfully loaded settings with fallback")
        print(f"   - Using default settings: {settings.default_name}")
    except Exception as e:
        print(f"   ❌ Error loading settings with fallback: {e}")


def _demonstrate_default_settings():
    """Demonstrate creating settings with default values."""
    print("3. Creating settings with default values:")
    try:
        # Import required enums
        from domain.greeting.models.greeting_language import GreetingLanguage
        from domain.greeting.models.greeting_type import GreetingType
        from infrastructure.models.settings.environment import Environment

        default_settings = Settings(
            project_env=Environment.DEV,
            default_name="World",
            greeting_type=GreetingType.BASIC,
            greeting_language=GreetingLanguage.EN,
            web_framework="FastAPI",
        )
        print("   ✅ Created default settings")
        print(f"   - Project environment: {default_settings.project_env}")
        print(f"   - Default name: {default_settings.default_name}")
        print(f"   - Web framework: {default_settings.web_framework}")
        print(f"   - Host: {default_settings.host}")
        print(f"   - Port: {default_settings.port}")
    except Exception as e:
        print(f"   ❌ Error creating default settings: {e}")


def _demonstrate_backward_compatibility():
    """Demonstrate backward compatibility features."""
    print("4. Backward compatibility demonstration:")
    print("   - All existing settings fields are preserved")
    print("   - Default values are provided for backward compatibility")
    print("   - New configuration sections are optional")
    print("   - Helper methods provide easy access to nested configurations")


def main():
    """Demonstrate the refactored settings functionality"""
    print("=== Settings Refactoring Example ===\n")

    # Example 1: Load settings from development.yml
    _demonstrate_development_yml_loading()

    print("\n" + "=" * 50 + "\n")

    # Example 2: Load settings with fallback
    _demonstrate_fallback_loading()

    print("\n" + "=" * 50 + "\n")

    # Example 3: Create settings with default values
    _demonstrate_default_settings()

    print("\n" + "=" * 50 + "\n")

    # Example 4: Demonstrate backward compatibility
    _demonstrate_backward_compatibility()

    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
