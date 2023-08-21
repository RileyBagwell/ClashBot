from src.league.match.Ban import Ban
from src.league.match.Objectives import Objectives


def initBans(bansList):
    bans = []
    for obj in bansList:
        bans.append(Ban(obj))
    return bans


class MatchTeam:
    def __init__(self, TeamDto):
        self.bans = initBans(TeamDto['bans'])
        self.objectives = Objectives(TeamDto['objectives'])
        self.teamId = TeamDto['teamId']
        self.win = TeamDto['win']
