from src.league.clash.TournamentPhase import TournamentPhase


def init_schedule(tourn_list):
    tourn_phases = []
    for obj in tourn_list:
        tourn_phases.append(TournamentPhase(obj))
    return tourn_phases


class Tournament:
    def __init__(self, tournament_dto):
        self.id = tournament_dto['id']
        self.theme_id = tournament_dto['themeId']
        self.name_key = tournament_dto['nameKey']
        self.name_key_secondary = tournament_dto['nameKeySecondary']
        self.schedule = init_schedule(tournament_dto['schedule'])
