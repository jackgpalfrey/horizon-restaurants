import time
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .env import get_env

CONNECTION_RETRY_LIMIT = 5
CONNECTION_RETRY_DELAY = 2


class Database:
    """
    Handles database connection and initialization
    All methods are static do not try to instantiate
    Must run both connect() and init() before usage

    Also runs all sql files in src/init_sql on init
    """

    connection: psycopg2.extensions.connection

    @classmethod
    def connect(cls) -> None:
        """ 
        Connect to database as defined in env
        Should be run once and only once

        NOTE: Database.init MUST be run after this to fully setup database
        """

        cls.host = "db"
        cls.port = get_env("DB_PORT")
        cls.dbname = get_env("DB_NAME")
        cls.user = get_env("DB_USER")
        cls.password = get_env("DB_PASSWORD")
        cls.connection_tries = 0

        print(f"Connecting to database on {cls.host}:{cls.port}")
        cls._verify_db_exists()

    @classmethod
    def init(cls) -> None:
        """
        Initialize database ( runs init_sql)
        Should be run once and only once
        """
        cls._run_sql_in_dir("src/init_sql")

    @classmethod
    def execute_and_commit(cls, query: str, *vars: tuple) -> None:
        """
        Execute given query
        """

        cur = cls.cursor()
        cur.execute(query, vars)
        cls.commit()

    @classmethod
    def execute_and_fetchone(cls, query: str, *vars: tuple) -> tuple | None:
        """
        Execute given query and return one row
        """

        cur = cls.cursor()
        cur.execute(query, vars)
        return cur.fetchone()

    @classmethod
    def execute_and_fetchall(cls, query: str, *vars: tuple) -> list[tuple]:
        """
        Execute given query and return all rows
        """

        cur = cls.cursor()
        cur.execute(query, vars)
        return cur.fetchall()

    @classmethod
    def execute(cls, query: str, *vars: tuple) -> psycopg2.extensions.cursor:
        """
        Execute given query and return cursor
        """

        cur = cls.cursor()
        cur.execute(query, vars)
        return cur

    @classmethod
    def cursor(cls) -> psycopg2.extensions.cursor:
        return cls.connection.cursor()

    @classmethod
    def commit(cls) -> None:
        cls.connection.commit()

    @classmethod
    def close(cls) -> None:
        cls.connection.close()

    @classmethod
    def is_connected(cls) -> bool:
        connection_exists = cls.connection is not None
        if connection_exists:
            return cls.connection.closed == 0

        return False

    @classmethod
    def DEBUG_delete_all_tables(cls, verify: str) -> None:
        """
        Delete all tables in database
        verify must be "DANGEROUSLY DELETE ALL TABLES"
        """

        if verify != "DANGEROUSLY DELETE ALL TABLES":
            raise Exception("You must verify that you want to delete all tables \
                            in the database by passing the string 'DANGEROUSLY DELETE ALL TABLES'  \
                            as the first argument to this function")

        cur = cls.cursor()
        cur.execute("DROP SCHEMA public CASCADE;")
        cur.execute("CREATE SCHEMA public;")
        cur.execute("GRANT ALL ON SCHEMA public TO postgres;")
        cur.execute("GRANT ALL ON SCHEMA public TO public;")
        cls.commit()

    @classmethod
    def _create_db_connection(cls, dbname: str) -> None:
        """
        Create a database connection to given dbname
        Sets that database to cls.connection
        """

        cls.connection_tries += 1
        try:
            cls.connection = psycopg2.connect(
                dbname=dbname,
                user=cls.user,
                password=cls.password,
                host=cls.host,
                port=cls.port
            )
        except psycopg2.OperationalError as e:
            if cls.connection_tries > CONNECTION_RETRY_LIMIT:
                raise e

            print(
                f"Failed to connect to database {dbname} on {cls.host}:{cls.port}. Retrying...")
            time.sleep(CONNECTION_RETRY_DELAY)
            cls._create_db_connection(dbname)

    @classmethod
    def _verify_db_exists(cls) -> None:
        """
        Check if database defined by cls.dbname exists and create it if it doesn't
        """

        dbname = cls.dbname
        database_exists = cls._check_database_exists(dbname)

        if not database_exists:
            print(f"Database {dbname} does not exist. Creating it now...")
            cls._create_database(dbname)

        cls.close()
        cls._create_db_connection(dbname)

    @classmethod
    def _check_database_exists(cls, dbname: str) -> bool:
        """
        Checks if given database exists
        WARNING: This method will change cls.connection to the postgres db
        """
        cls._create_db_connection("postgres")
        cur = cls.execute("SELECT datname FROM pg_database;")
        all_databases = cur.fetchall()

        return (dbname,) in all_databases

    @classmethod
    def _create_database(cls, dbname: str) -> None:
        cls.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cls.execute_and_commit("CREATE DATABASE "+dbname+";")
        print("Database created successfully")

    @classmethod
    def _run_sql_in_dir(cls, path: str) -> bool:
        """
        Runs all sql files in given directory
        """

        dir = os.scandir(path)
        sorted_dir = sorted(dir, key=lambda file: file.name)

        for file in sorted_dir:
            if file.is_dir():
                cls._run_sql_in_dir(file.path)
            else:
                cls._run_sql_file(file.path)

        dir.close()

    @classmethod
    def _run_sql_file(cls, path: str) -> bool:
        """
        Runs given sql file
        """

        print(f"Running sql file {path}")
        file = open(path, "r")
        sql = file.read()

        cls.execute_and_commit(sql)

        file.close()
        print(f"Successfully ran sql file {path}")
