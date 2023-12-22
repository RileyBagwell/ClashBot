import os

import requests
import asyncio
import httpx

from src.league.LeagueEntry import LeagueEntry
from src.league.Summoner import Summoner
from src.league.clash.Team import Team
from src.league.clash.Tournament import Tournament
from src.utils.errors import RiotRateLimit


class RiotRequestHandler:
    def __init__(self):
        self.riotKey = os.getenv('RIOT_KEY')


    def raise_riot_exception(self, response):
        code = response.status_code
        if code == 429:
            raise RiotRateLimit("Rate limit exceeded")


    # ----- Summoner functions
    def getSummonerByName(self, region, name):
        """Obtain a summoner given a Region object and name. Returns a Summoner object."""
        url = f'https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getSummonerByName(): {response.status_code}, {response.reason}')
            return None
        return Summoner(response.json(), region)  # Create and return a Summoner object with SummonerDTO


    def getSummonerById(self, region, id):
        """Obtain a summoner given a Region object and name. Returns a Summoner object."""
        url = f'https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getSummonerById(): {response.status_code}, {response.reason}')
            return None
        return Summoner(response.json(), region)  # Create and return a Summoner object with SummonerDTO


    def getLeagueEntryBySummonerId(self, region, id):
        """Obtain a summoner's rank information given a region and name. Returns a list of LeagueEntry objects."""
        print("league entry")
        url = f'https://{region.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getLeagueEntryBySummonerId(): {response.status_code}, {response.reason}')
            return None
        leagueList = [None, None]
        for obj in response.json():
            if obj['queueType'] == 'RANKED_SOLO_5x5':
                leagueList[0] = LeagueEntry(obj)
            elif obj['queueType'] == 'RANKED_FLEX_SR':
                leagueList[1] = LeagueEntry(obj)
        print("returning league entry")
        return leagueList


    # ----- Match functions
    async def getMatchesFromList(self, region, matchIdList, matchList):
        """Populates a given (empty) matchList to contain a list of match data as json objects.
        Top level function."""
        await self.async_getMatchesFromList(region, matchIdList, matchList)


    async def async_getMatchesFromList(self, region, matchIdList, matchList):
        """Helper function for getMatchesFromList(). Creates the asyncio tasks."""
        tasks = [self.async_getMatch(region, matchId) for matchId in matchIdList]
        matchList.extend(await asyncio.gather(*tasks))  # Await the results and extend the existing matchList


    async def async_getMatch(self, region, matchId):
        """Helper function for getMatchesFromList().
        Returns a match's data as a json object given its match id."""
        url = f'https://{region.route}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.riotKey}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None


    def getMatchIdListByPuuid(self, region, puuid, numMatches):
        """Obtain a given number of matchIds for a specified puuid. Returns a list of matchIds."""
        url = f'https://{region.route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={numMatches}&api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchesByPuuid(): {response.status_code}, {response.reason}')
            return None
        return list(response.json())


    def getMatchByMatchId(self, regionObj, matchId):
        """Obtain match data given a region and matchId. Returns a Match json object."""
        print("getMatchByMatchId() start")
        url = f'https://{regionObj.route}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchByMatchId(): {response.status_code}, {response.reason}')
            return None
        print("End")
        return response.json()


    # ----- Clash functions
    def getTournaments(self, region):
        """Obtain all active or upcoming tournaments. Returns a list of  Tournament objects."""
        url = f'https://{region.region}.api.riotgames.com/lol/clash/v1/tournaments?api_key={self.riotKey}'
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

    def getTeamByTeamId(self, region, teamId):
        """Obtain team information given a region and teamId. Returns a Team object."""
        url = f'https://{region.region}.api.riotgames.com/lol/clash/v1/teams/{teamId}?api_key={self.riotKey}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamByTeamId(): {response.status_code}, {response.reason}')
            return None
        return Team(response.json())
