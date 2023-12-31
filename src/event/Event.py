class Event:
    def __init__(self, event_id: str):
        self._event_id = event_id

    def get_id(self) -> str:
        return self._event_id
