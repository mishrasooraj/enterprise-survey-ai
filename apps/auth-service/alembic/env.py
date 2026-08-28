from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import make_url

# ======================================================
# Add src/ to Python path
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

# ======================================================
# Application Imports
# ======================================================

from app.core.core_config import settings
from app.db.db_base import Base

# Import all models so SQLAlchemy registers them
import app.db.models.organization
import app.db.models.permission
import app.db.models.role
import app.db.models.role_permission
import app.db.models.user

# ======================================================
# Alembic Configuration
# ======================================================

config = context.config

database_url = make_url(settings.database.url)
# The line below incorrectly overrides the database host to 'localhost',
# which fails inside a Docker container. It's commented out to allow
# the correct host ('postgres') from the .env file to be used.
# database_url = database_url.set(host="localhost")

config.set_main_option(
    "sqlalchemy.url",
    database_url.render_as_string(hide_password=False),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata


# ======================================================
# Offline Migrations
# ======================================================

def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ======================================================
# Online Migrations
# ======================================================

def run_migrations_online() -> None:
    """Run migrations in online mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ======================================================
# Entry Point
# ======================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
