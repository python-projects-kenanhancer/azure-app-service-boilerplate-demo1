# Ovo Kenan Boilerplate Demo1

Author: Kenan Hancer <kenan.hancer@ovo.com>

Azure App Service Python Application

## Clean Architecture Overview

![Architecture Overview](./images/clean_architecture.png)

## Key Features

1. HTTP API Endpoints

   - RESTful API endpoints for handling HTTP requests and responses.
   - Health check endpoint for Azure App Service monitoring.
   - Clean separation of concerns with use cases and domain logic.

1. Centralized Configuration Management

   - Load and inject environment variables from a local `.env`, `config.json` or `config.yaml` file.
   - Load and inject environment variables from `Azure Storage`, `Azure Key Vault` so that settings of application will be centralized

1. Dependency Management and Testing

   - UV is used for efficient dependency management and packaging.
   - Pytest provides a simple and flexible framework for writing and running tests, ensuring reliability and consistency of your Azure App Service.

> Note: This project is designed for Azure App Service deployment with Python 3.12 support.

______________________________________________________________________

## Prerequisites

### Required Programs

Before setting up this project, ensure the following programs are installed:

### Docker (Optional - for local development)

For local development with PostgreSQL and Redis, install Docker:

```bash
# macOS
brew install --cask docker

# Or download from https://www.docker.com/products/docker-desktop
```

### Required Programs

### Xcode CLI

To use homebrew to install Python packages, you need a compiler

```bash
xcode-select --install
```

### Homebrew

Homebrew is a package manager for macOS, used to install other tools like `asdf` and `jq`.

Installation:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### jq

jq is a lightweight and flexible command-line JSON processor, used for automating JSON file generation.

Installation:

```bash
brew install jq
```

### asdf

asdf is a version manager for multiple runtimes like Python, Node.js, Java, Go, etc.

Installation:

```bash
brew install asdf
```

- Add asdf to your shell by adding the following lines to your shell configuration (~/.zshrc or ~/.bashrc):

  For `~/.zshrc`:

  ```bash
  echo '. $(brew --prefix asdf)/libexec/asdf.sh' >> ~/.zshrc
  ```

  For `~/.bashrc`:

  ```bash
  echo '. $(brew --prefix asdf)/libexec/asdf.sh' >> ~/.bashrc
  ```

- After adding the line, reload the shell configuration file for the changes to take effect:

  For `~/.zshrc`:

  ```bash
  source ~/.zshrc
  ```

  For `~/.bashrc`:

  ```bash
  source ~/.bashrc
  ```

### python

- Install the Python plugin and Python 3.12.7 using asdf:

  ```bash
  asdf plugin add python
  asdf install python 3.12.7
  asdf global python 3.12.7
  ```

- Verify the installation:

  ```bash
  python --version
  ```

### UV

- UV is a fast Python package installer and resolver, written in Rust. Install it using pip:

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Azure CLI

- Install Azure CLI running the following commands. Find more details in [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

  ```bash
  brew install azure-cli
  ```

- To initialize the Azure CLI, run az login:

  ```bash
  az login
  ```

- Verify the installation:

  ```bash
  az --version
  ```

### Automating VS Code Extensions Setup

- Install VSCode Default Extensions programatically.

  ```bash
  cat .vscode/extensions.json | jq -r '.recommendations[]' | xargs -n 1 code --install-extension
  ```

## Setting Up the Project

1. Clone the Repository:

   ```bash
   git clone <repository-url>
   cd ovo_kenan_boilerplate_demo1
   ```

1. Configure application settings:

   **Option A: Using config.json (Currently Active)**

   The application is configured to use `config.json` by default. You can modify this file to change settings:

   ```json
   {
     "project_env": "local",
     "default_name": "World",
     "greeting_type": "time_based",
     "greeting_language": "en",
     "web_framework": "fastapi",
     "host": "0.0.0.0",
     "port": 8000,
     "debug": true
   }
   ```

   **Option B: Using .env file**

   Create a `.env` file in the root directory:

   ```bash
   PROJECT_ENV=local
   DEFAULT_NAME=World
   GREETING_TYPE=time_based
   GREETING_LANGUAGE=en
   WEB_FRAMEWORK=fastapi
   HOST=0.0.0.0
   PORT=8000
   DEBUG=true
   AZURE_KEYVAULT_URL=https://app-keyvault-dev.vault.azure.net/
   AZURE_STORAGE_ACCOUNT_URL=https://ovokenanboilerplatedevstorage.blob.core.windows.net/
   ```

   Note: If you want to use `.env`, you'll need to update `src/infrastructure/dependency_injection_configurations/build_di_container.py` to use `EnvConfigLoaderArgs` instead of `JsonConfigLoaderArgs`.

1. Create and Activate Virtual Environment:

   ```bash
   uv venv
   source .venv/bin/activate  # For Linux/Mac
   ```

1. Install Dependencies:

   ```bash
   # Install all dependencies including dev dependencies
   uv sync

   # Install/Reinstall pre-commit hooks
   rm -rf .git/hooks/*  # Remove all git hooks
   uv run pre-commit clean # Clean any existing pre-commit
   uv run pre-commit uninstall # Uninstall any remaining hooks
   uv run pre-commit install --overwrite  # Install hooks fresh
   ```

   or

   ```bash
   uv run setup
   ```

1. Run Tests: Run the tests using pytest:

   ```bash
   uv run pytest
   ```

1. Sync after team members update dependencies

   ```bash
   git pull # Get latest changes
   uv sync # Update environment from uv.lock
   ```

## Running Pre-commit hooks

- This command executes all the pre-commit hooks defined in your .pre-commit-config.yaml file on all files in your repository, regardless of whether they have been modified or staged for commit. It ensures that your entire codebase adheres to the standards and checks specified by your pre-commit hooks.

  ```bash
  # Run all pre-commit hooks
  uv run pre-commit run --all-files

  # OR

  # Run with verbose output
  uv run pre-commit run --all-files --verbose
  ```

- Additional Command Options

  ```bash
  # Run specific hooks
  uv run pre-commit run black --all-files
  uv run pre-commit run pretty-format-json --all-files
  uv run pre-commit run pretty-format-json --files config.json
  ```

## Local Development with Docker Compose

For local development with PostgreSQL and Redis, you can use the included Docker Compose setup:

### Quick Start

```bash
# Start all services (PostgreSQL, Redis, pgAdmin, Redis Commander)
./scripts/docker-compose-helper.sh start

# Check service status
./scripts/docker-compose-helper.sh status

# View logs
./scripts/docker-compose-helper.sh logs

# Stop services
./scripts/docker-compose-helper.sh stop
```

### Services Available

- **PostgreSQL**: `localhost:5432` (Database: `azure_app_service_db`)
- **Redis**: `localhost:6379` (Cache and session store)
- **pgAdmin**: http://localhost:8080 (PostgreSQL web interface)
- **Redis Commander**: http://localhost:8081 (Redis web interface)

### Database Connection

```bash
# PostgreSQL
postgresql://app_user:app_password@localhost:5432/azure_app_service_db

# Redis
redis://localhost:6379/0
```

### Web Interface Credentials

- **pgAdmin**: `admin@azure-app-service.com` / `admin123`
- **Redis Commander**: `admin` / `admin123`

For more details, see [DOCKER_COMPOSE_README.md](./DOCKER_COMPOSE_README.md).

## Testing Azure App Service

- List App Services

  ```bash
  az webapp list --resource-group ovo-kenan-boilerplate-dev-rg
  ```

- How to Get Logs for an App Service

  ```bash
  az webapp log tail --name ovo-kenan-boilerplate-dev-app --resource-group ovo-kenan-boilerplate-dev-rg
  ```

  OR

  ```bash
  az webapp log show --name ovo-kenan-boilerplate-dev-app --resource-group ovo-kenan-boilerplate-dev-rg
  ```

- Test App Service

  ```bash
  curl -X POST https://ovo-kenan-boilerplate-dev-app.azurewebsites.net/say_hello \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe"
  }'
  ```

- Health Check

  ```bash
  curl https://ovo-kenan-boilerplate-dev-app.azurewebsites.net/health
  ```

## Terraform Deployment from local for **terraform**

```bash
cd ./ovo_kenan_boilerplate_demo1
source ./scripts/init_terraform.sh
init_terraform terraform-state-bucket-for-boilerplate "GrEs/8Y9T6c8XHppgSClVMopJuXH17XakvmgxHCmawo=" terraform
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

## Local Development

To run the application locally:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the Flask application
python -m src.main
```

The application will be available at `http://localhost:8000`

## API Endpoints

- `POST /say_hello` - Main greeting endpoint
- `GET /health` - Health check endpoint for Azure App Service monitoring
