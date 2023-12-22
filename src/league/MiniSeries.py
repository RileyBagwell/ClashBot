class MiniSeries:
    def __init__(self, mini_series_dto):
        self.losses = mini_series_dto['losses']
        self.progress = mini_series_dto['progress']
        self.target = mini_series_dto['target']
        self.wins = mini_series_dto['wins']
