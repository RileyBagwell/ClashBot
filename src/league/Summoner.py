class Summoner:
    def __init__(self, SummonerDTO, region):
        """Create a Summoner object given a SummonerDTO and Region object from the API"""
        self.region = region
        self.accountId = SummonerDTO['accountId']
        self.profileIconId = SummonerDTO['profileIconId']
        self.revisionDate = SummonerDTO['revisionDate']
        self.name = SummonerDTO['name']
        self.id = SummonerDTO['id']
        self.puuid = SummonerDTO['puuid']
        self.summonerLevel = SummonerDTO['summonerLevel']


    def __str__(self):
        """Returns a neatly formatted string containing summoner information"""
        return f'Name: {self.name}\nLevel: {self.summonerLevel}\npuuid: {self.puuid}\nid: {self.id}'
