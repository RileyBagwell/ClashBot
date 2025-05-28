"""
Contains team information for a match.
"""
from dataclasses import dataclass
from typing import List, Optional
from src.league.match.Ban import Ban
from src.league.match.Objectives import Objectives

@dataclass
class Ban:
    championId: int
    pickTurn: int

@dataclass
class Objective:
    first: bool
    kills: int

@dataclass
class Objectives:
    baron: Objective
    champion: Objective
    dragon: Objective
    horde: Objective
    inhibitor: Objective
    riftHerald: Objective
    tower: Objective

def init_bans(bans_list):
    bans = []
    for obj in bans_list:
        bans.append(Ban(obj))
    return bans

class MatchTeam:
    def __init__(self, team_dto=None):
        if team_dto is None:
            self.bans = []
            self.objectives = None
            self.team_id = None
            self.win = False
            return

        # If team_dto is a tuple from database
        if isinstance(team_dto, tuple):
            iterator = iter(team_dto)
            self.team_id = next(iterator)
            self.win = next(iterator)
            self.bans = []  # Will be populated separately
            self.objectives = None  # Will be populated separately
            return

        # If team_dto is from Riot API
        self.team_id = team_dto.get('teamId')
        self.win = team_dto.get('win', False)
        
        # Initialize bans
        self.bans = []
        for ban_dto in team_dto.get('bans', []):
            self.bans.append(Ban(
                championId=ban_dto.get('championId'),
                pickTurn=ban_dto.get('pickTurn')
            ))

        # Initialize objectives
        objectives_dto = team_dto.get('objectives', {})
        self.objectives = Objectives(
            baron=Objective(
                first=objectives_dto.get('baron', {}).get('first', False),
                kills=objectives_dto.get('baron', {}).get('kills', 0)
            ),
            champion=Objective(
                first=objectives_dto.get('champion', {}).get('first', False),
                kills=objectives_dto.get('champion', {}).get('kills', 0)
            ),
            dragon=Objective(
                first=objectives_dto.get('dragon', {}).get('first', False),
                kills=objectives_dto.get('dragon', {}).get('kills', 0)
            ),
            horde=Objective(
                first=objectives_dto.get('horde', {}).get('first', False),
                kills=objectives_dto.get('horde', {}).get('kills', 0)
            ),
            inhibitor=Objective(
                first=objectives_dto.get('inhibitor', {}).get('first', False),
                kills=objectives_dto.get('inhibitor', {}).get('kills', 0)
            ),
            riftHerald=Objective(
                first=objectives_dto.get('riftHerald', {}).get('first', False),
                kills=objectives_dto.get('riftHerald', {}).get('kills', 0)
            ),
            tower=Objective(
                first=objectives_dto.get('tower', {}).get('first', False),
                kills=objectives_dto.get('tower', {}).get('kills', 0)
            )
        )
