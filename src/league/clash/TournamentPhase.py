class TournamentPhase:
    def __init__(self, TournamentPhaseDto):
        self.id = TournamentPhaseDto['id']
        self.registrationTime = TournamentPhaseDto['registrationTime']
        self.startTime = TournamentPhaseDto['startTime']
        self.cancelled = TournamentPhaseDto['cancelled']
