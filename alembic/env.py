# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import sys

from alembic import context
from logging.config import fileConfig

dir_current = os.path.split(os.path.abspath(__file__))[0]
dir_parent = os.path.abspath(os.path.join(dir_current, os.pardir))
sys.path.append(dir_parent)

from pubmed_ingester.config import import_config
from pubmed_ingester.dal_base import DalBase
from pubmed_ingester.orm_base import Base

cfg = import_config(
    fname_config_file="/etc/pubmed-ingester/pubmed-ingester.json"
)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

dal = DalBase(
    sql_username=cfg.sql_username,
    sql_password=cfg.sql_password,
    sql_host=cfg.sql_host,
    sql_port=cfg.sql_port,
    sql_db=cfg.sql_db,
)

config.set_main_option(
    name="sqlalchemy.url",
    value=dal.create_url()
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
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
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = dal.engine

    with engine.connect() as connection:
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
