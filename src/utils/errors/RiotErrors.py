class RiotAPIException(Exception):
    """Base class for Riot API exceptions."""
    def __init__(self, status_code=None, message="An error occurred while making a request to the Riot API"):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return str(f"{self.__class__.__name__}: {self.message}. Status Code: {self.status_code}")


class RiotBadRequest(RiotAPIException):
    def __init__(self, status_code=400, message="Bad request made to Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotUnauthorizedRequest(RiotAPIException):
    def __init__(self, status_code=401, message="Unauthorized request made to Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotForbiddenRequest(RiotAPIException):
    def __init__(self, status_code=403, message="Forbidden request made to Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotDataNotFound(RiotAPIException):
    def __init__(self, status_code=404, message="Data not found from Riot API request"):
        super().__init__(status_code=status_code, message=message)


class RiotMethodNotAllowed(RiotAPIException):
    def __init__(self, status_code=405, message="Method not allowed by Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotUnsupportedMediaType(RiotAPIException):
    def __init__(self, status_code=415, message="Unsupported media type in Riot API request"):
        super().__init__(status_code=status_code, message=message)


class RiotRateLimit(RiotAPIException):
    def __init__(self, status_code=429, message="Rate limit exceeded to Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotInternalServerError(RiotAPIException):
    def __init__(self, status_code=500, message="Internal server error from Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotBadGateway(RiotAPIException):
    def __init__(self, status_code=502, message="Bad gateway error from Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotServiceUnavailable(RiotAPIException):
    def __init__(self, status_code=503, message="Service unavailable from Riot API"):
        super().__init__(status_code=status_code, message=message)


class RiotGatewayTimeout(RiotAPIException):
    def __init__(self, status_code=504, message="Gateway timeout from Riot API"):
        super().__init__(status_code=status_code, message=message)
