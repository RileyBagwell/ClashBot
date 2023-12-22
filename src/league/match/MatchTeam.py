from src.league.match.Ban import Ban
from src.league.match.Objectives import Objectives


def init_bans(bans_list):
    bans = []
    for obj in bans_list:
        bans.append(Ban(obj))
    return bans


class MatchTeam:
    def __init__(self, team_dto):
        self.bans = init_bans(team_dto['bans'])
        self.objectives = Objectives(team_dto['objectives'])
        self.team_id = team_dto['teamId']
        self.win = team_dto['win']
