#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=== Running Database Migrations ==="
echo

# Activate virtual environment if it exists
if [[ -f .venv/bin/activate ]]; then
    source .venv/bin/activate
fi

# Check if alembic is available
if ! command -v alembic &> /dev/null; then
    echo "Error: alembic not found. Please run ./scripts/bootstrap.sh first"
    exit 1
fi

# Run migrations
echo "Applying migrations..."
alembic upgrade head

echo
echo "=== Migrations complete! ==="