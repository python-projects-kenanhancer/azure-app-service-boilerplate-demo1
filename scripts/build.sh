#!/bin/bash

# Build script for Azure App Service deployment

set -e

echo "Building application for Azure App Service deployment..."

# Create dist directory if it doesn't exist
mkdir -p dist

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/*

# Generate requirements.txt from pyproject.toml
echo "Generating requirements.txt..."
uv pip compile pyproject.toml -o requirements.txt

# Create deployment package
echo "Creating deployment package..."
zip -r dist/app.zip . \
    -x "*.git*" \
    -x "*.venv*" \
    -x "*.pytest_cache*" \
    -x "*.vscode*" \
    -x "*.idea*" \
    -x "*.tox*" \
    -x "*.coverage*" \
    -x "*.cache*" \
    -x "*.log*" \
    -x "*.pyc*" \
    -x "__pycache__*" \
    -x "tests*" \
    -x "terraform*" \
    -x "scripts*" \
    -x "images*" \
    -x "*.rest*" \
    -x "*.md*" \
    -x "*.toml*" \
    -x "*.lock*"

echo "Build completed successfully!"
echo "Deployment package created at: dist/app.zip"
echo "Size: $(du -h dist/app.zip | cut -f1)"
