class MiniSeries:
    def __init__(self, MiniSeriesDto):
        self.losses = MiniSeriesDto['losses']
        self.progress = MiniSeriesDto['progress']
        self.target = MiniSeriesDto['target']
        self.wins = MiniSeriesDto['wins']
