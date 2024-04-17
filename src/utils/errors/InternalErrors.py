class ClashBotException(Exception):
    def __init__(self, status_code=None, message="An internal error has occurred."):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return str(f"{self.__class__.__name__}: {self.message}. Status Code: {self.status_code}")
