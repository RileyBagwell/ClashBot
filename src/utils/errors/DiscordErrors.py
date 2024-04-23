class DiscordAPIException(Exception):
    """Base class for Discord API exceptions."""
    def __init__(self, status_code=None, message="An error occurred while making a request to the Discord API"):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return str(f"{self.__class__.__name__}: {self.message}. Status Code: {self.status_code}")


class InvalidRiotID(DiscordAPIException):
    def __init__(self, status_code=501, message="Given Riot ID is invalid"):
        super().__init__(status_code=status_code, message=message)