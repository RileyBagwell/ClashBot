class Ban:
    def __init__(self, BanDto):
        self.championId = BanDto['championId']
        self.pickTurn = BanDto['pickTurn']
