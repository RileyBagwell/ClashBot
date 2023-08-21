"""
    Contains all information for a match.
"""
from src.league.match.MatchTeam import MatchTeam
from src.league.match.Participant import Participant


class Match:
    def __init__(self, MatchDto):
        metadata = MatchDto['metadata']
        info = MatchDto['info']
        # metadata
        self.dataVersion = metadata['dataVersion']
        self.matchId = metadata['matchId']
        self.participants = metadata['participants']  # List of puuids
        # info
        self.gameDuration = info['gameDuration']
        self.gameEndTimestamp = info['gameEndTimestamp']
        self.gameId = info['gameId']
        self.gameMode = info['gameMode']
        self.gameName = info['gameName']
        self.gameStartTimestamp = info['gameStartTimestamp']
        self.gameType = info['gameType']
        self.gameVersion = info['gameVersion']
        self.mapId = info['mapId']
        self.participants = self.initParticipants(info['participants'])
        self.platformId = info['platformId']
        self.queueId = info['queueId']
        self.teams = self.initTeams(info['teams'])
        self.tournamentCode = info['tournamentCode']


    def initParticipants(self, participantsDtoList):
        participants = []
        for obj in participantsDtoList:
            participants.append(Participant(obj))
        return participants


    def initTeams(self, teamsDtoList):
        teams = []
        for obj in teamsDtoList:
            teams.append(MatchTeam(obj))
        return teams
