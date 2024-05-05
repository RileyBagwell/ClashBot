class LeagueEntry:
    def __init__(self, league_entry_dto):
        self.league_id = league_entry_dto['leagueId']
        self.summoner_id = league_entry_dto['summonerId']
        self.queue_type = league_entry_dto['queueType']
        self.tier = league_entry_dto['tier']
        self.rank = league_entry_dto['rank']
        self.league_points = league_entry_dto['leaguePoints']
        self.wins = league_entry_dto['wins']
        self.losses = league_entry_dto['losses']
        self.hot_streak = league_entry_dto['hotStreak']
        self.veteran = league_entry_dto['veteran']
        self.fresh_blood = league_entry_dto['freshBlood']
        self.inactive = league_entry_dto['inactive']


    def winrate(self):
        """Calculates and returns the winrate."""
        if self.losses == 0:
            return 100
        total = self.total_games()
        return round((self.wins / total) * 100)


    def total_games(self):
        """Returns the total number of games played."""
        return self.wins + self.losses


    def __str__(self):
        return (f'Queue Type: {self.queue_type}  |  Hot StreaK: {self.hot_streak}  |  Veteran: {self.veteran}\n'
                f'Fresh Blood: {self.fresh_blood}  |  Inactive: {self.inactive}\n'
                f'{self.tier} {self.rank} - {self.league_points} LP\n'
                f'{self.wins}W {self.losses}L - Winrate: {self.winrate()}%\n')
