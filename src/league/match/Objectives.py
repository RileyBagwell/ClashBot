from src.league.match.Objective import Objective


class Objectives:
    def __init__(self, objectives_dto):
        self.baron = Objective(objectives_dto['baron'])
        self.champion = Objective(objectives_dto['champion'])
        self.dragon = Objective(objectives_dto['dragon'])
        self.inhibitor = Objective(objectives_dto['inhibitor'])
        self.rift_herald = Objective(objectives_dto['riftHerald'])
        self.tower = Objective(objectives_dto['tower'])
