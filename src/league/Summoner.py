class Summoner:
    """A class to represent a Summoner object from the Riot API.
    Attributes:
        region (Region): The region of the summoner.
        account_id (str): The account ID of the summoner.
        profile_icon_id (int): The profile icon ID of the summoner.
        revision_date (int): The revision date of the summoner.
        id (str): The ID of the summoner.
        puuid (str): The PUUID of the summoner.
        summoner_level (int): The summoner level of the summoner."""


    def __init__(self, summoner_dto, region):
        """Create a Summoner object given a SummonerDTO and Region object from the API"""
        self.region = region
        self.account_id = summoner_dto['accountId']
        self.profile_icon_id = summoner_dto['profileIconId']
        self.revision_date = summoner_dto['revisionDate']
        self.id = summoner_dto['id']
        self.puuid = summoner_dto['puuid']
        self.summoner_level = summoner_dto['summonerLevel']


    def __str__(self):
        """Returns a neatly formatted string containing summoner information"""
        return f'Level {self.summoner_level} (ID: {self.id})'
