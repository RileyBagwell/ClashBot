class Summoner:
    def __init__(self, summoner_dto, region):
        """Create a Summoner object given a SummonerDTO and Region object from the API"""
        self.region = region
        self.account_id = summoner_dto['accountId']
        self.profile_icon_id = summoner_dto['profileIconId']
        self.revision_date = summoner_dto['revisionDate']
        self.name = summoner_dto['name']
        self.id = summoner_dto['id']
        self.puuid = summoner_dto['puuid']
        self.summoner_level = summoner_dto['summonerLevel']


    def __str__(self):
        """Returns a neatly formatted string containing summoner information"""
        return f'Name: {self.name}\nLevel: {self.summoner_level}\npuuid: {self.puuid}\nid: {self.id}'
