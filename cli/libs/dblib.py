from src.utils.Database import Database


def dbConnect() -> bool:
    """
    Usage: dbConnect
    """

    Database.connect()
    return True


def dbInit() -> bool:
    """
    Usage: dbInit
    """
    if not Database.is_connected():
        print("Not connected to database. Use dbConnect first.")
        return

    Database.init()
    return True


def dbDisconnect() -> bool:
    """
    Usage: dbDisconnect
    """
    if not Database.is_connected():
        print("Not connected to database. Use dbConnect first.")
        return

    Database.disconnect()
    return True


def dbQuery(query: str, *vars) -> list[tuple]:
    """
    Usage: dbQuery <query> [...vars]
    """
    if not Database.is_connected():
        print("Not connected to database. Use dbConnect first.")
        return

    return Database.execute_and_fetchall(query, vars)


def dbQueryOne(query: str, *vars) -> tuple | None:
    """
    Usage: dbQueryOne <query> [...vars]
    """
    if not Database.is_connected():
        print("Not connected to database. Use dbConnect first.")
        return

    return Database.execute_and_fetchone(query, vars)


def dbExecute(query: str, *vars) -> None:
    """
    Usage: dbExecute <query> [...vars]
    """
    if not Database.is_connected():
        print("Not connected to database. Use dbConnect first.")
        return

    Database.execute_and_commit(query, vars)
    return
