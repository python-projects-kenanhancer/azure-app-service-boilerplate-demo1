#!/bin/bash

print_usage() {
    echo "Description:"
    echo "  Initializes Terraform configuration with remote state backend configuration"
    echo
    echo "Usage:"
    echo "  init_terraform <bucket-name> <encryption-key> <terraform-dir>"
    echo
    echo "Arguments:"
    echo "  bucket-name    Name of the S3 bucket for Terraform state storage"
    echo "  encryption-key Key used for state file encryption"
    echo "  terraform-dir  Directory containing Terraform configuration files"
    echo
    echo "Example:"
    echo "  init_terraform my-terraform-state my-encryption-key terraform"
}

init_terraform() {
    if [ "$#" -ne 3 ]; then
        print_usage
        return 1
    fi

    local BUCKET_NAME=$1
    local ENCRYPTION_KEY=$2
    local TERRAFORM_DIR=$3

    # Determine the absolute path of the script
    local SCRIPT_PATH="$(
        cd "$(dirname "${BASH_SOURCE[0]}")" || exit
        pwd -P
    )"

    # Find the project root by looking for a distinctive directory
    local ROOT_DIR="$(cd "$SCRIPT_PATH" && while [[ "$PWD" != "/" ]]; do
        if [[ -d "$TERRAFORM_DIR" && -d "scripts" ]]; then
            pwd
            break
        fi
        cd ..
    done)"

    # Get repository info
    local REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))
    local DEVELOPER_NAME=${GITHUB_ACTOR:-$(git config user.name | tr ' ' '_')}
    local TARGET_DIR="$ROOT_DIR/$TERRAFORM_DIR"
    local BACKEND_CONFIG="$TARGET_DIR/backend-config.hcl"
    local SCRIPTS_DIR="$ROOT_DIR/scripts"
    local TFVAR_FILE="$TARGET_DIR/terraform.tfvars"
    local BRANCH_NAME=""

    # Check if we're on a tag
    if [ -n "$(git tag --points-at HEAD)" ]; then
        BRANCH_NAME="refs/tags/$(git tag --points-at HEAD)"
    else
        BRANCH_NAME="refs/heads/$(git rev-parse --abbrev-ref HEAD)"
    fi

    echo "REPO_NAME: $REPO_NAME"
    echo "DEVELOPER_NAME: $DEVELOPER_NAME"
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "ROOT_DIR: $ROOT_DIR"
    echo "TARGET_DIR: $TARGET_DIR"
    echo "TERRAFORM_DIR: $TERRAFORM_DIR"
    echo "BACKEND_CONFIG: $BACKEND_CONFIG"
    echo "SCRIPTS_DIR: $SCRIPTS_DIR"

    # Validate terraform directory exists
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Error: Directory $TERRAFORM_DIR not found"
        return 1
    fi

    # Source the environment config script with correct path
    source "$SCRIPTS_DIR/get_environment_config.sh"

    # Get state prefix from environment config
    output=$(get_environment_config "$REPO_NAME/$TERRAFORM_DIR" "$BRANCH_NAME" "$DEVELOPER_NAME")
    echo "Full output: $output"

    SKIP=$(echo "$output" | grep "skip" | cut -d'=' -f2)

    if [ "$SKIP" != "true" ]; then
        STATE_PREFIX=$(echo "$output" | grep "state_prefix" | cut -d'=' -f2)
        echo "STATE_PREFIX: $STATE_PREFIX"

        echo "$BACKEND_CONFIG is being generated:"

        cat >"$BACKEND_CONFIG" <<EOF
bucket = "$BUCKET_NAME"
prefix = "$STATE_PREFIX"
encryption_key = "$ENCRYPTION_KEY"
EOF

        echo "$BACKEND_CONFIG is generated:"
        cat $BACKEND_CONFIG

        # Set ENVIRONMENT in terraform.tfvars
        ENVIRONMENT=$(echo "$output" | grep "environment_name" | cut -d'=' -f2 | tr '_' '-')
        echo "ENVIRONMENT: $ENVIRONMENT"

        echo "$TFVAR_FILE is being generated:"
        # Use GNU sed for compatibility across different systems
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS sed
            sed -i '' "s/environment *=.*\"/environment = \"$ENVIRONMENT\"/I" $TFVAR_FILE
        else
            # Linux/GNU sed
            sed -i "s/environment *=.*\"/environment = \"$ENVIRONMENT\"/I" $TFVAR_FILE
        fi

        echo "$TFVAR_FILE is generated:"
        cat $TFVAR_FILE

        # Initialize terraform with generated backend config
        terraform -chdir=$TARGET_DIR init -reconfigure -backend-config="$BACKEND_CONFIG"
    fi
}
