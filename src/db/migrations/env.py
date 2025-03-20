import asyncio

from alembic.autogenerate import rewriter
from alembic.operations import ops
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import Column, Connection
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.core.constants.app import AppConstants

from src.db.models import *

config = context.config

config.set_main_option("sqlalchemy.url", AppConstants.db_url)

target_metadata = UserDB.metadata

writer = rewriter.Rewriter()


@writer.rewrites(ops.CreateTableOp)
def order_columns(
    context: EnvironmentContext,
    revision: tuple[str, ...],
    op: ops.CreateTableOp,
) -> ops.CreateTableOp:
    """Orders ID first and the audit columns at the end."""
    special_names = {
        "id": -100,
        "sa_orm_sentinel": 3001,
        "created_at": 3002,
        "updated_at": 3002,
    }
    cols_by_key = [
        (
            special_names.get(col.key, index) if isinstance(col, Column) else 2000,
            col.copy(),  # type: ignore[attr-defined]
        )
        for index, col in enumerate(op.columns)
    ]
    columns = [col for _, col in sorted(cols_by_key, key=lambda entry: entry[0])]
    return ops.CreateTableOp(
        op.table_name,
        columns,
        schema=op.schema,
        # Remove when https://github.com/sqlalchemy/alembic/issues/1193 is fixed
        _namespace_metadata=op._namespace_metadata,
        **op.kw,
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
