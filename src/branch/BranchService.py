from ..utils.Database import Database
from ..branch.Branch import Branch


class BranchService:
    @staticmethod
    def create(branch_name: str, address: str) -> Branch:
        Database.execute_and_commit(
            "INSERT INTO public.branch (name, address) VALUES(%s, %s)", branch_name, address)

        # branch_id = Database.execute_and_fetchone("SELECT id FROM public.branch WHERE name = %s", branch_name)
        # return Branch(branch_id)
        return BranchService.get_by_name(branch_name)

    @staticmethod
    def get_by_name(branch_name: str) -> Branch:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE name = %s", branch_name)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_by_id(branch_id: str) -> Branch:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE id = %s", branch_id)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_all() -> Branch:
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.branch")

        if result is not None:
            return [Branch(record[0]) for record in result]
