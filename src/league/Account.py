class Account:
    def __init__(self, account_dto, region):
        """Create a Summoner object given a SummonerDTO and Region object from the API"""
        self.region = region
        self.puuid = account_dto['puuid']
        if account_dto['gameName'] is None:
            self.name = 'GameName'
        else:
            self.name = account_dto['gameName']
        if account_dto['tagLine'] is None:
            self.tag_line = 'TagLine'
        else:
            self.tag_line = account_dto['tagLine']
        self.name_tag = f'{self.name}#{self.tag_line}'


    def __str__(self):
        """Returns a neatly formatted string containing summoner information"""
        return f'Account Name: {self.name}#{self.tag_line} with puuid: {self.puuid}'
