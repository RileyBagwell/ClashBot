from src.league.clash.TournamentPhase import TournamentPhase


def initSchedule(tournList):
    tournPhases = []
    for obj in tournList:
        tournPhases.append(TournamentPhase(obj))
    return tournPhases


class Tournament:
    def __init__(self, TournamentDto):
        self.id = TournamentDto['id']
        self.themeId = TournamentDto['themeId']
        self.nameKey = TournamentDto['nameKey']
        self.nameKeySecondary = TournamentDto['nameKeySecondary']
        self.schedule = initSchedule(TournamentDto['schedule'])
