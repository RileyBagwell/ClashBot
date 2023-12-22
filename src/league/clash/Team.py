"""
    Contains all information for a Clash team
"""
from src.league.clash.Player import Player


class Team:
    def __init__(self, TeamDto):
        self.id = TeamDto['id']
        self.tournamentId = TeamDto['tournamentId']
        self.name = TeamDto['name']
        self.iconId = TeamDto['iconId']
        self.tier = TeamDto['tier']
        self.captain = TeamDto['captain']
        self.abbreviation = TeamDto['abbreviation']
        self.players = self.initPlayers(TeamDto['players'])


    def __str__(self):
        return (f'Team name: {self.name}\nAbbreviation: {self.abbreviation}\nCaptain: {self.captain}\nTeam ID: {self.id}\n'
                f'Tier: {self.tier}\n')


    def initPlayers(self, playersList):
        players = []
        for obj in playersList:
            players.append(Player(obj, self.id))
        return players
