"""
    Contains information for players on a clash team.
"""


class Player:
    def __init__(self, PlayerDto, teamId):
        self.summonerId = PlayerDto['summonerId']
        self.teamId = teamId
        self.position = PlayerDto['position']
        self.role = PlayerDto['role']
