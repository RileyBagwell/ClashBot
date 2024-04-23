import os
from typing import List, Optional

import requests
import asyncio
import httpx

from src.league.Account import Account
from src.league.LeagueEntry import LeagueEntry
from src.league.Region import Region
from src.league.Summoner import Summoner
from src.league.clash.Team import Team
from src.league.clash.Tournament import Tournament
from src.utils.errors.RiotErrors import RiotBadRequest, RiotUnauthorizedRequest, RiotForbiddenRequest, \
    RiotDataNotFound, RiotMethodNotAllowed, RiotUnsupportedMediaType, RiotRateLimit, RiotInternalServerError, \
    RiotBadGateway, RiotServiceUnavailable, RiotGatewayTimeout, RiotAPIException


class RiotRequestHandler:
    """
    Class to handle requests to the Riot API.

    Attributes:
        riot_key: The Riot API key to make requests to the API
    """
    def __init__(self):
        self.riot_key = os.getenv('RIOT_KEY')


    def validate_status_code(self, code) -> bool:
        """Check status code from response and raise exception if necessary. Returns True if code is 200.
        Otherwise, raises an exception. It is unnecessary to check for 200 status codes in the calling function."""
        if code == 200:
            return True
        exceptions = {
            400: RiotBadRequest,
            401: RiotUnauthorizedRequest,
            403: RiotForbiddenRequest,
            404: RiotDataNotFound,
            405: RiotMethodNotAllowed,
            415: RiotUnsupportedMediaType,
            429: RiotRateLimit,
            500: RiotInternalServerError,
            502: RiotBadGateway,
            503: RiotServiceUnavailable,
            504: RiotGatewayTimeout
        }

        exception_class = exceptions.get(code)
        if exception_class is None:
            exception_class = RiotAPIException
        raise exception_class()


    # ----- Account functions
    def get_account_by_riot_id(self, region, riot_id) -> Optional[Account]:
        """Obtain an account given a Region object, game name, and tag line."""
        url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id.name}/{riot_id.tag_line}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_account_by_riot_id(): {e}")
            return None
        return Account(response.json(), region)  # Create and return an Account object with AccountDTO


    # ----- Summoner functions
    def get_summoner_by_name(self, region, name):
        """Obtain a summoner given a Region object and name. Returns a Summoner object."""
        url = f'https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in getSummonerByName(): {e}")
            return None
        return Summoner(response.json(), region)  # Create and return a Summoner object with SummonerDTO


    def get_summoner_by_account(self, region: Region, account: Account):
        """Obtain a summoner given a Region object and name. Returns a Summoner object."""
        url = f'https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{account.puuid}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_summoner_by_account(): {e}")
            return None
        return Summoner(response.json(), region, account)  # Create and return a Summoner object with SummonerDTO


    def get_league_entry_by_summoner_id(self, region, id):
        """Obtain a summoner's rank information given a region and name. Returns a list of LeagueEntry objects."""
        url = f'https://{region.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getLeagueEntryBySummonerId(): {response.status_code}, {response.reason}')
            return None
        league_list = [None, None]
        for obj in response.json():
            if obj['queueType'] == 'RANKED_SOLO_5x5':
                league_list[0] = LeagueEntry(obj)
            elif obj['queueType'] == 'RANKED_FLEX_SR':
                league_list[1] = LeagueEntry(obj)
        return league_list


    # ----- Match functions
    async def get_matches_from_list(self, region, match_id_list, match_list):
        """Populates a given (empty) matchList to contain a list of match data as json objects.
        Top level function."""
        try:
            await self.async_get_matches_from_list(region, match_id_list, match_list)
        except Exception as e:
            print(f"Error in getMatchesFromList(): {e}")


    async def async_get_matches_from_list(self, region, match_id_list, match_list):
        """Helper function for getMatchesFromList(). Creates the asyncio tasks."""
        try:
            tasks = [self.async_get_match(region, match_id) for match_id in match_id_list]
            match_list.extend(await asyncio.gather(*tasks))  # Await the results and extend the existing matchList
        except RiotRateLimit as e:
            print(f"Error in getMatchesFromList(): {e}")


    async def async_get_match(self, region, match_id):
        """Helper function for getMatchesFromList().
        Returns a match's data as a json object given its match id."""
        url = f'https://{region.route}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.riot_key}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                print(f"Returning match data: {match_id}   |   {response.json}")
                return response.json()
            else:
                print(f'Error in getMatch(): {response.status_code}, {response.json}')
                raise RiotRateLimit


    def get_match_id_list_by_puuid(self, region, puuid, num_matches) -> List[str]:
        """Obtain a given number of matchIds for a specified puuid. Returns a list of matchIds."""
        url = f'https://{region.route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num_matches}&api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchesByPuuid(): {response.status_code}, {response.reason}')
            return None
        print("Returning list of match IDs")
        return list(response.json())


    def get_match_by_match_id(self, region_obj, match_id)  -> dict:
        """Obtain match data given a region and matchId. Returns a Match json object."""
        print("getMatchByMatchId() start")
        url = f'https://{region_obj.route}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getMatchByMatchId(): {response.status_code}, {response.reason}')
            return None
        print("End")
        return response.json()


    # ----- Clash functions
    def get_tournaments(self, region) -> List[Tournament]:
        """Obtain all active or upcoming tournaments. Returns a list of  Tournament objects."""
        url = f'https://{region.region}.api.riotgames.com/lol/clash/v1/tournaments?api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTournaments(): {response.status_code}, {response.reason}')
            return None
        tournaments = []
        for obj in response.json():
            tournaments.append(Tournament(obj))
        return tournaments


    def get_team_ids_by_summoner_id(self, region_obj, id) -> List[str]:
        """Obtain team ids given a region and summoner name. Returns a list of team_ids."""
        url = f'https://{region_obj.region}.api.riotgames.com/lol/clash/v1/players/by-summoner/{id}?api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamIdsBySummonerId(): {response.status_code}, {response.reason}')
            return None
        team_ids = []
        for obj in response.json():
            team_ids.append(obj['teamId'])
        return team_ids

    def get_team_by_team_id(self, region, team_id) -> Team:
        """Obtain team information given a region and teamId. Returns a Team object."""
        url = f'https://{region.region}.api.riotgames.com/lol/clash/v1/teams/{team_id}?api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamByTeamId(): {response.status_code}, {response.reason}')
            return None
        return Team(response.json())
