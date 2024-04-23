from src.utils.errors.DiscordErrors import InvalidRiotID


class RiotID:
    """A class to represent a Riot ID.

    Attributes:
        name: A string representing the name of the account.
        tag_line: A string representing the tag of the account.
        is_valid: A boolean representing if the Riot ID is valid.
    """

    def __init__(self, riot_id: str):
        """Constructs a RiotID object.

        Args:
            riot_id: A string representing the Riot ID.
        """
        split = riot_id.split('#')
        if len(split) != 2:
            self.name = ""
            self.tag_line = ""
            self.is_valid = False
        else:
            self.name = split[0]
            self.tag_line = split[1]
            self.is_valid = True


    def __str__(self) -> str:
        """Returns the RiotID object as a string."""
        return f"{self.name}#{self.tag_line}"
