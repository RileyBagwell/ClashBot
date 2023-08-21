class LeagueEntry:
    def __init__(self, LeagueEntryDto):
        self.leagueId = LeagueEntryDto['leagueId']
        self.summonerId = LeagueEntryDto['summonerId']
        self.summonerName = LeagueEntryDto['summonerName']
        self.queueType = LeagueEntryDto['queueType']
        self.tier = LeagueEntryDto['tier']
        self.rank = LeagueEntryDto['rank']
        self.leaguePoints = LeagueEntryDto['leaguePoints']
        self.wins = LeagueEntryDto['wins']
        self.losses = LeagueEntryDto['losses']
        self.hotStreak = LeagueEntryDto['hotStreak']
        self.veteran = LeagueEntryDto['veteran']
        self.freshBlood = LeagueEntryDto['freshBlood']
        self.inactive = LeagueEntryDto['inactive']


    def winrate(self):
        """Calculates and returns the winrate."""
        if self.losses == 0:
            return 100
        total = self.totalGames()
        return round((self.wins / total) * 100)


    def totalGames(self):
        """Returns the total number of games played."""
        return self.wins + self.losses
