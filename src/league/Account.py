class Summoner:
    def __init__(self, account_dto, region):
        """Create a Summoner object given a SummonerDTO and Region object from the API"""
        self.puuid = account_dto['puuid']
        self.game_name = account_dto['gameName']
        self.tag_line = account_dto['tagLine']



    def __str__(self):
        """Returns a neatly formatted string containing summoner information"""
        return f'Name: {self.name}\nLevel: {self.summoner_level}\npuuid: {self.puuid}\nid: {self.id}'
