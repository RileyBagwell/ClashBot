"""
    Contains all information for a Clash team
"""
from src.league.clash.Player import Player


class Team:
    def __init__(self, team_dto):
        self.id = team_dto['id']
        self.tournament_id = team_dto['tournamentId']
        self.name = team_dto['name']
        self.icon_id = team_dto['iconId']
        self.tier = team_dto['tier']
        self.captain = team_dto['captain']
        self.abbreviation = team_dto['abbreviation']
        self.players = self.init_players(team_dto['players'])


    def __str__(self):
        return (f'Team name: {self.name}\nAbbreviation: {self.abbreviation}\nCaptain: {self.captain}\nTeam ID: {self.id}\n'
                f'Tier: {self.tier}\n')


    def init_players(self, players_list):
        players = []
        for obj in players_list:
            players.append(Player(obj, self.id))
        return players
