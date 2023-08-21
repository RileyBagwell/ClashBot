import os

import requests

from src.league.LeagueEntry import LeagueEntry
from src.league.Summoner import Summoner
from src.league.clash.Team import Team
from src.league.clash.Tournament import Tournament
from src.league.match.Match import Match


def rerouteRegion(region):
    """Reroute a given region. Ex: 'na1' -> 'americas'"""
    region = region.lower()
    americas = {'na1', 'br1', 'la1', 'la2'}
    europe = {'euw1', 'eun1', 'tr1', 'ru'}
    asia = {'jp1', 'kr'}
    sea = {'oc1', 'ph2', 'sg2', 'th2', 'tw2', 'vn2'}
    if region in americas:
        return 'americas'
    if region in europe:
        return 'europe'
    if region in asia:
        return 'asia'
    if region in sea:
        return 'sea'
    return region


class RiotRequestHandler:
    def __init__(self):
        self.riotKey = os.getenv('RIOT_KEY')


    # ----- Summoner functions
    def getSummonerByName(self, region, name):
        """Obtain a summoner given a region and name. Returns a Summoner object."""
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getSummonerByName(): {response.status_code}, {response.reason}')
            return None
        return Summoner(response.json())  # Create and return a Summoner object with SummonerDTO


    def getSummonerById(self, region, id):
        """Obtain a summoner given a region and name. Returns a Summoner object."""
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getSummonerById(): {response.status_code}, {response.reason}')
            return None
        return Summoner(response.json())  # Create and return a Summoner object with SummonerDTO


    def getPuuidByName(self, region, name):
        """Obtain a summoner's PUUID given a region and name. Returns the puuid as a string. Returns None if summoner
        is not found."""
        summoner = self.getSummonerByName(region, name)
        if summoner is None:
            return None
        return summoner.puuid


    def getSummonerIdByName(self, region, name):
        """Obtain a summoner's id given a region and name. Returns a summonerId"""
        summoner = self.getSummonerByName(region, name)
        if summoner is None:
            return None
        return summoner.id


    def getLeagueEntryBySummonerId(self, region, id):
        """Obtain a summoner's rank information given a region and name. Returns a list of LeagueEntry objects."""
        url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.riotKey}'
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
    def getMatchesByPuuid(self, region, puuid, numMatches):
        """Obtain a given number of matchIds for a specified puuid. Returns a list of matchIds."""
        if region.lower() == 'na1':
            region = 'americas'
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numMatches}&api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchesByPuuid(): {response.status_code}, {response.reason}')
            return None
        return list(response.json())


    def getMatchByMatchId(self, region, matchId):
        """Obtain match data given a region and matchId. Returns a Match object."""
        if region.lower() == 'na1':
            region = 'americas'
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchByMatchId(): {response.status_code}, {response.reason}')
            return None
        return Match(response.json())


    # ----- Clash functions
    def getTournaments(self, region):
        """Obtain all active or upcoming tournaments. Returns a list of  Tournament objects."""
        url = f'https://{region}.api.riotgames.com/lol/clash/v1/tournaments?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTournaments(): {response.status_code}, {response.reason}')
            return None
        tournaments = []
        for obj in response.json():
            tournaments.append(Tournament(obj))
        return tournaments


    def getTeamIdsBySummonerId(self, region, id):
        """Obtain team ids given a region and summoner name. Returns a list of teamIds."""
        url = f'https://{region}.api.riotgames.com/lol/clash/v1/players/by-summoner/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamIdsBySummonerId(): {response.status_code}, {response.reason}')
            return None
        teamIds = []
        for obj in response.json():
            teamIds.append(obj['teamId'])
        return teamIds

    def getTeamByTeamId(self, region, teamId):
        """Obtain team information given a region and teamId. Returns a Team object."""
        url = f'https://{region}.api.riotgames.com/lol/clash/v1/teams/{teamId}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamByTeamId(): {response.status_code}, {response.reason}')
            return None
        return Team(response.json())
