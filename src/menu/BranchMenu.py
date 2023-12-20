"""A class responsible for handling Menu actions."""


class BranchMenu:
    """Accessible via Branch.menu."""

    def __init__(self, branch_id: str):
        """Dont call outside of Branch."""
        self._branch_id = branch_id
