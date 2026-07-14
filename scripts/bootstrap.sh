#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=== Prism Intelligence Bootstrap ==="
echo

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.12"
if ! python3 -c "import sys; exit(import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1))"; then
    echo "Error: Python 3.12+ is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment if it doesn't exist
if [[ ! -d .venv ]]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev,test]"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Create .env from example if it doesn't exist
if [[ ! -f .env ]]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠ Please update .env with your configuration"
fi

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo
    echo "Docker is available. Starting services..."
    docker-compose -f docker/docker-compose.yml up -d postgres redis

    echo "Waiting for services to be healthy..."
    sleep 5

    # Run migrations
    echo "Running database migrations..."
    ./scripts/migrate.sh
else
    echo
    echo "⚠ Docker not found. Please start PostgreSQL and Redis manually:"
    echo "  PostgreSQL: postgresql://prism:prism@localhost:5432/prism"
    echo "  Redis: redis://localhost:6379/0"
    echo "Then run: ./scripts/migrate.sh"
fi

echo
echo "=== Bootstrap complete! ==="
echo
echo "To start the API server:"
echo "  source .venv/bin/activate"
echo "  uvicorn prism.interfaces.api.main:app --reload"
echo
echo "To start the Celery worker:"
echo "  source .venv/bin/activate"
echo "  celery -A prism.infrastructure.celery.app worker --loglevel=info"
echo
echo "To run tests:"
echo "  source .venv/bin/activate"
echo "  pytest tests/ -v"