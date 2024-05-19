"""
    Contains all information for a match.
"""
from src.league.match.MatchTeam import MatchTeam
from src.league.match.Participant import Participant


class Match:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def deserialize_match(self, columns, match_tuple):
        match_data = dict(zip(columns, match_tuple))
        return Match()

        # metadata
        self.data_version = match_json['dataVersion']
        self.match_id = metadata['matchId']
        # info
        self.game_creation = match_json['gameCreation']
        self.game_duration = info['gameDuration']
        self.game_end_timestamp = info['gameEndTimestamp']
        self.game_id = info['gameId']
        self.game_mode = info['gameMode']
        self.game_name = info['gameName']
        self.game_start_timestamp = info['gameStartTimestamp']
        self.game_type = info['gameType']
        self.game_version = info['gameVersion']
        self.map_id = info['mapId']
        self.platform_id = info['platformId']
        self.queue_id = info['queueId']
        #self.teams = self.init_teams(info['teams'])
        self.tournament_code = info['tournamentCode']


    def init_participants(self, participants_dto_list):
        participants = []
        for obj in participants_dto_list:
            participants.append(Participant(obj))
        return participants


    def init_teams(self, teams_dto_list):
        teams = []
        for obj in teams_dto_list:
            teams.append(MatchTeam(obj))
        return teams
