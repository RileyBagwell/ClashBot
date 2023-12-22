from src.league.match.Objective import Objective


class Objectives:
    def __init__(self, ObjectivesDto):
        self.baron = Objective(ObjectivesDto['baron'])
        self.champion = Objective(ObjectivesDto['champion'])
        self.dragon = Objective(ObjectivesDto['dragon'])
        self.inhibitor = Objective(ObjectivesDto['inhibitor'])
        self.riftHerald = Objective(ObjectivesDto['riftHerald'])
        self.tower = Objective(ObjectivesDto['tower'])
