from ..utils.Database import Database
from ..branch.Branch import Branch

class BranchService:
    @staticmethod
    def create(branch_name: str, address: str) -> Branch:
        Database.execute_and_commit("INSERT INTO branch (name, address) VALUES(%s, %s)", branch_name, address)
        # branch_id = Database.execute_and_fetchone("SELECT id FROM public.branch WHERE name = %s", branch_name)
        # return Branch(branch_id)
        return BranchService.get_by_name(branch_name)
        
    @staticmethod
    def get_by_name(branch_name: str) -> Branch:
        branch_id = Database.execute_and_fetchone("SELECT id FROM public.branch WHERE name = %s", branch_name)
        return Branch(branch_id)