import psycopg2

from src.utils.Database import Database


def test_database_connection():
    Database.connect()
    assert Database.connection is not None


def test_can_delete_tables():
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")


def test_can_run_init_sql():
    Database.init()
    cur = Database.cursor()
    cur.execute("INSERT INTO init_check_table VALUES ('init_check', 1);")
    Database.commit()
    cur.execute("SELECT * FROM init_check_table;")
    assert cur.fetchall() == [('init_check', 1)]


def test_can_create_table():
    cur = Database.cursor()
    sql = """
        CREATE TABLE test_table
        (
            name text,
            age integer,
            PRIMARY KEY (name)
        );
    """
    cur.execute(sql)
    Database.commit()
    cur.execute("SELECT * FROM test_table;")
    assert cur.fetchall() == []


def test_can_insert_into_table():
    cur = Database.cursor()
    sql = "INSERT INTO test_table VALUES ('test', 1);"
    cur.execute(sql)
    Database.commit()
    cur.execute("SELECT * FROM test_table;")
    assert cur.fetchall() == [('test', 1)]


def test_execute_and_commit():
    Database.execute_and_commit(
        "INSERT INTO test_table VALUES ('execommit', 1);")
    cur = Database.cursor()
    cur.execute("SELECT * FROM test_table WHERE name = %s;", ('execommit',))
    assert cur.fetchall() == [('execommit', 1)]


def test_execute_and_fetchone():
    row = Database.execute_and_fetchone(
        "SELECT * FROM test_table WHERE name = %s;", 'execommit')
    assert row == ('execommit', 1)


def test_execute_and_fetchall():
    rows = Database.execute_and_fetchall("SELECT * FROM test_table;")
    assert rows == [('test', 1), ('execommit', 1)]


def test_execute():
    cur = Database.execute("SELECT * FROM test_table;")
    assert cur.fetchall() == [('test', 1), ('execommit', 1)]


def test_can_close_connection():
    Database.close()
    assert Database.connection.closed == 1
