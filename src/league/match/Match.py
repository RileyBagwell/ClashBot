"""
    Contains all information for a match based on Riot's Match-V5 API.
"""
from src.league.match.MatchTeam import MatchTeam
from src.league.match.Participant import Participant


class Match:
    def __init__(self, m=None):
        if m is None:
            # Initialize with default values when creating empty match
            self.data_version = None
            self.match_id = None
            self.participants_puuid = []  # List of participant PUUIDs from metadata
            # Info fields
            self.end_of_game_result = None
            self.game_creation = None
            self.game_duration = None
            self.game_end_timestamp = None
            self.game_id = None
            self.game_mode = None
            self.game_name = None
            self.game_start_timestamp = None
            self.game_type = None
            self.game_version = None
            self.map_id = None
            self.participants = []  # List of ParticipantDto objects
            self.platform_id = None
            self.queue_id = None
            self.teams = []  # List of TeamDto objects
            self.tournament_code = None
            return

        # If m is a tuple from database
        if isinstance(m, tuple):
            iterator = iter(m)
            self.data_version = next(iterator)
            self.match_id = next(iterator)
            self.end_of_game_result = next(iterator)
            self.game_creation = next(iterator)
            self.game_duration = next(iterator)
            self.game_end_timestamp = next(iterator)
            self.game_id = next(iterator)
            self.game_mode = next(iterator)
            self.game_name = next(iterator)
            self.game_start_timestamp = next(iterator)
            self.game_type = next(iterator)
            self.game_version = next(iterator)
            self.map_id = next(iterator)
            self.platform_id = next(iterator)
            self.queue_id = next(iterator)
            self.tournament_code = next(iterator)
            self.participants = []  # Will be populated separately
            self.teams = []  # Will be populated separately
            return

        # If m is a dictionary from Riot API
        metadata = m.get('metadata', {})
        info = m.get('info', {})
        
        # Metadata fields
        self.data_version = metadata.get('dataVersion')
        self.match_id = metadata.get('matchId')
        self.participants_puuid = metadata.get('participants', [])

        # Info fields
        self.end_of_game_result = info.get('endOfGameResult')
        self.game_creation = info.get('gameCreation')
        self.game_duration = info.get('gameDuration')
        self.game_end_timestamp = info.get('gameEndTimestamp')
        self.game_id = info.get('gameId')
        self.game_mode = info.get('gameMode')
        self.game_name = info.get('gameName')
        self.game_start_timestamp = info.get('gameStartTimestamp')
        self.game_type = info.get('gameType')
        self.game_version = info.get('gameVersion')
        self.map_id = info.get('mapId')
        self.platform_id = info.get('platformId')
        self.queue_id = info.get('queueId')
        self.tournament_code = info.get('tournamentCode')

        # Initialize participants and teams
        self.participants = self.init_participants(info.get('participants', []))
        self.teams = self.init_teams(info.get('teams', []))

    def init_participants(self, participants_dto_list):
        """Initialize list of Participant objects from DTO data."""
        participants = []
        for obj in participants_dto_list:
            participants.append(Participant(obj))
        return participants

    def init_teams(self, teams_dto_list):
        """Initialize list of MatchTeam objects from DTO data."""
        teams = []
        for obj in teams_dto_list:
            teams.append(MatchTeam(obj))
        return teams
