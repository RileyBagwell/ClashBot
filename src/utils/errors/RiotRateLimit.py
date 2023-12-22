class RiotRateLimit:
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return str(self.message)
        else:
            return self.__class__.__name__
