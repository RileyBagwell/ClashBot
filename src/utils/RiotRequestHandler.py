import os

import requests

from src.league.clash.LeagueEntry import LeagueEntry
from src.league.Summoner import Summoner
from src.league.clash.Team import Team
from src.league.clash.Tournament import Tournament
from src.league.match.Match import Match


class RiotRequestHandler:
    def __init__(self):
        self.riotKey = os.getenv('RIOT_KEY')


    # ----- Summoner functions
    def getSummonerByName(self, regionObj, name):
        """Obtain a summoner given a Region object and name. Returns a Summoner object."""
        url = f'https://{regionObj.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getSummonerByName(): {response.status_code}, {response.reason}')
            return None
        return Summoner(response.json())  # Create and return a Summoner object with SummonerDTO


    def getSummonerById(self, regionObj, id):
        """Obtain a summoner given a Region object and name. Returns a Summoner object."""
        url = f'https://{regionObj.region}.api.riotgames.com/lol/summoner/v4/summoners/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getSummonerById(): {response.status_code}, {response.reason}')
            return None
        return Summoner(response.json())  # Create and return a Summoner object with SummonerDTO


    def getPuuidByName(self, regionObj, name):
        """Obtain a summoner's PUUID given a region and name. Returns the puuid as a string. Returns None if summoner
        is not found."""
        summoner = self.getSummonerByName(regionObj, name)
        if summoner is None:
            return None
        return summoner.puuid


    def getSummonerIdByName(self, regionObj, name):
        """Obtain a summoner's id given a region and name. Returns a summonerId"""
        summoner = self.getSummonerByName(regionObj, name)
        if summoner is None:
            return None
        return summoner.id


    def getLeagueEntryBySummonerId(self, regionObj, id):
        """Obtain a summoner's rank information given a region and name. Returns a list of LeagueEntry objects."""
        url = f'https://{regionObj.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchesByPuuid(): {response.status_code}, {response.reason}')
            return None
        leagueList = [0] * 2
        for obj in response.json():
            if obj['queueType'] == 'RANKED_SOLO_5x5':
                leagueList[0] = LeagueEntry(obj)
            elif obj['queueType'] == 'RANKED_FLEX_SR':
                leagueList[1] = LeagueEntry(obj)
        return leagueList


    # ----- Match functions
    def getMatchesByPuuid(self, regionObj, puuid, numMatches):
        """Obtain a given number of matchIds for a specified puuid. Returns a list of matchIds."""
        url = f'https://{regionObj.route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numMatches}&api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchesByPuuid(): {response.status_code}, {response.reason}')
            return None
        return list(response.json())


    def getMatchByMatchId(self, regionObj, matchId):
        """Obtain match data given a region and matchId. Returns a Match object."""
        url = f'https://{regionObj.route}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchByMatchId(): {response.status_code}, {response.reason}')
            return None
        return Match(response.json())


    # ----- Clash functions
    def getTournaments(self, regionObj):
        """Obtain all active or upcoming tournaments. Returns a list of  Tournament objects."""
        url = f'https://{regionObj.region}.api.riotgames.com/lol/clash/v1/tournaments?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTournaments(): {response.status_code}, {response.reason}')
            return None
        tournaments = []
        for obj in response.json():
            tournaments.append(Tournament(obj))
        return tournaments


    def getTeamIdsBySummonerId(self, regionObj, id):
        """Obtain team ids given a region and summoner name. Returns a list of teamIds."""
        url = f'https://{regionObj.region}.api.riotgames.com/lol/clash/v1/players/by-summoner/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamIdsBySummonerId(): {response.status_code}, {response.reason}')
            return None
        teamIds = []
        for obj in response.json():
            teamIds.append(obj['teamId'])
        return teamIds

    def getTeamByTeamId(self, regionObj, teamId):
        """Obtain team information given a region and teamId. Returns a Team object."""
        url = f'https://{regionObj.region}.api.riotgames.com/lol/clash/v1/teams/{teamId}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamByTeamId(): {response.status_code}, {response.reason}')
            return None
        return Team(response.json())
