class Summoner:
    def __init__(self, SummonerDTO):
        """Create a Summoner object given a SummonerDTO from the API"""
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
