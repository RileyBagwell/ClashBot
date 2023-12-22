class TournamentPhase:
    def __init__(self, tournament_phase_dto):
        self.id = tournament_phase_dto['id']
        self.registration_time = tournament_phase_dto['registrationTime']
        self.start_time = tournament_phase_dto['startTime']
        self.cancelled = tournament_phase_dto['cancelled']
