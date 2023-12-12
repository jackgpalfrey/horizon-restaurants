class HorizonError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class AlreadyExistsError(HorizonError):
    pass


class AuthenticationError(HorizonError):
    pass


class AuthorizationError(HorizonError):
    pass
