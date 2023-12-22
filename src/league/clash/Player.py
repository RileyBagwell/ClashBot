"""
    Contains information for players on a clash team.
"""


class Player:
    def __init__(self, player_dto, team_id):
        self.summoner_id = player_dto['summonerId']
        self.team_id = team_id
        self.position = player_dto['position']
        self.role = player_dto['role']
