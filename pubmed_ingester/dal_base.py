# -*- coding: utf-8 -*-

""" Boilerplate SQLAlchemy to SQL-server interaction module.

This module contains the `DalBase` class which is meant to facilitate safe
interaction between SQLAlchemy and SQL-servers.
"""

import inspect
import contextlib

import decorator
import sqlalchemy
import sqlalchemy.orm


class DalBase(object):
    """Basic Python boilerplate for interaction with an SQL database.

    Attributes:
        sql_user (str): SQL database username
        sql_password (str): SQL database password
        sql_host (str): SQL database hostname
        sql_port (str): SQL database port
        sql_dbname (str): SQL database name
        sql_url_template (str): SQL URL template containing the type of database
            and driver to be used for the connection.
    """

    def __init__(
        self,
        sql_username,
        sql_password,
        sql_host,
        sql_port,
        sql_db,
        sql_url_template=("postgresql+psycopg2://{username}:"
                          "{password}@{host}:{port}/{db}"),
        **kwargs
    ):
        """Initializes database connection and session"""

        # Internalize arguments.
        self.sql_username = sql_username
        self.sql_password = sql_password
        self.sql_host = sql_host
        self.sql_port = sql_port
        self.sql_db = sql_db
        self.sql_url_template = sql_url_template

        # Inspecting the presence of keyword arguments and (should they not be
        # defined) setting defaults.
        self.sql_engine_pool_size = kwargs.get("sql_engine_pool_size", 1)
        self.sql_engine_pool_recycle = kwargs.get(
            "sql_engine_pool_recycle", 3600
        )
        self.sql_engine_echo = kwargs.get("sql_engine_echo", False)
        self.expire_on_commit = kwargs.get("expire_on_commit", False)

        # create DB engine.
        self.engine = self.connect()

        # create new session.
        self.session_factory = sqlalchemy.orm.sessionmaker(
            bind=self.engine,
            expire_on_commit=self.expire_on_commit
        )

    def create_url(self):
        """Renders the database URL for the given template"""

        # Format the template strings with the user credentials and host
        # information provided upon instantiation.
        url = self.sql_url_template
        url = url.format(
            username=self.sql_username,
            password=self.sql_password,
            host=self.sql_host,
            port=self.sql_port,
            db=self.sql_db
        )

        return url

    def connect(self, url=None):
        """Connects to the database and returns the SQLAlchemy engine

        Args:
            url (str): The database URL.

        Returns:
            sqlalchemy.engine.base.Engine: The SQLAlchemy connection engine.
        """

        # If no URL was provided then create one through `self.create_url`.
        if not url:
            url = self.create_url()

        # Create the engine.
        engine = sqlalchemy.create_engine(
            url,
            pool_size=self.sql_engine_pool_size,
            pool_recycle=self.sql_engine_pool_recycle,
            echo=self.sql_engine_echo,
        )

        # Connect to the database.
        engine.connect()

        return engine

    @contextlib.contextmanager
    def session_scope(self, expunge_objects=True, refresh_objects=False):
        """Provide a transactional scope around a series of operations

        Args:
            expunge_objects (bool, optional): Mark objects as detached from this
                session. Objects can then be read after the session terminates.
                Defaults to `True`.
            refresh_objects (bool, optional): Explicitly re-query objects after
                committing session. Defaults to `False`.

        Note:
            If `expunge_objects` is set to `False` then any database record ORM
            object either retrieved through queries performed through this
            session or objects added through this session can no longer be
            accessed after the session is closed. Doing so will raise a
            `DetachedInstance` exception.

        Yields:
            sqlalchemy.orm.session.Session: A new session established through
                `self.engine`.
        """

        # Create a new session.
        session = self.session_factory()

        try:
            # Yield the session and allow the caller to perform DB work.
            yield session

            # At this point the context-manager has closed. The session is
            # flushed and committed thus persisting changes to the database.
            session.flush()
            session.commit()
        # In the event of an exception the session is rolled back and the
        # exception is raised.
        except Exception as exc:
            session.rollback()
            raise exc
        # Close the session.
        finally:
            if refresh_objects:
                for obj in session:
                    session.refresh(obj)
            if expunge_objects:
                session.expunge_all()

            session.close()


def with_session_scope(**dec_kwargs):
    """Decorator factory, takes arguments accepted by the `session_scope` method
    of the `self` object of its wrapped function.

    This allows methods to declare that they want a session context, support a
    default way to make one, but still allow the caller to pass a preexisting
    session and control transaction scope.

    Note:
        Wrapped function must accept a defaultable `session` parameter, as well
        as a `self` parameter supporting the `sesson_scope` method.

        If call to wrapped function doesn't pass a session, will create a new
        session according to the args passed to the decorator factory.
        Otherwise, will leave session alone and become a noop.
    """

    @decorator.decorator
    def wrapper(target, *args, **kwargs):
        kwargs = inspect.getcallargs(target, *args, **kwargs)

        if "session" in kwargs and kwargs["session"]:
            return target(**kwargs)
        else:
            with kwargs["self"].session_scope(**dec_kwargs) as session:
                kwargs["session"] = session
                return target(**kwargs)

    return wrapper
