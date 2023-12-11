from .utils.Database import Database


class User:
    def __init__(self, user_id: str) -> None:
        self._user_id = user_id

    def delete(self) -> None:
        # FIXME: Could cause issues with references, might be best to switch to soft deletion and a cron job
        sql = """
        DELETE FROM public.user WHERE id=%s;
        """

        Database.execute_and_commit(sql, self._user_id)
