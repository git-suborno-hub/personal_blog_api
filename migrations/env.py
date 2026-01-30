import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

# তোমার মডেল import করো — এটা খুব গুরুত্বপূর্ণ!
from app.models import Base  # যদি Article model এখানে থাকে

# Alembic Config object
config = context.config

# logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# তোমার SQLAlchemy models-এর metadata — এটা None রাখলে কোনো টেবিল তৈরি হবে না
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # offline mode-এও env থেকে URL নেবো (ini-এর উপর নির্ভর না করে)
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL not set in environment variables!")

    print(f"Alembic offline using DATABASE_URL: {url}")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in environment variables!")

    print(f"Alembic online using DATABASE_URL: {db_url}")

    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()