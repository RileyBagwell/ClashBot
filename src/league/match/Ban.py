class Ban:
    def __init__(self, ban_dto):
        self.champion_id = ban_dto['championId']
        self.pick_turn = ban_dto['pickTurn']
