from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# NOTE: Base will be imported here once infrastructure/db/models is implemented.
# For now, target_metadata is None until Phase 2 models are created.
# from src.prism.infrastructure.db.models.base import Base
# target_metadata = Base.metadata
target_metadata = None

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

try:
    from src.prism.infrastructure.config import get_settings

    settings = get_settings()
    config.set_main_option("sqlalchemy.url", str(settings.database_url))
except Exception:
    pass  # Settings not available (e.g., offline generation)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()