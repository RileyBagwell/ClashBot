import os
import random
from typing import List, Optional

import requests
import asyncio
import httpx
from aiolimiter import AsyncLimiter

from src.league.Account import Account
from src.league.LeagueEntry import LeagueEntry
from src.league.Region import Region
from src.league.Summoner import Summoner
from src.league.clash.Player import Player
from src.league.clash.Team import Team
from src.league.clash.Tournament import Tournament
from src.league.match.Match import Match
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
        self.minute_limiter = AsyncLimiter(20, 120)  # 200 requests per minute
        self.second_limiter = AsyncLimiter(1, .05)  # 20 requests per second


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
    def get_account_by_puuid(self, region: Region, puuid: str) -> Optional[Account]:
        url = f"https://{region.route}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={self.riot_key}"
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_account_by_puuid(): {e}")
            return None

        account = None
        try:
            account = Account(response.json(), region)
        except Exception as e:
            print(f"Error in get_account_by_puuid(): {e}")
            return None
        return account


    def get_account_by_riot_id(self, region, riot_id) -> Optional[Account]:
        """Obtain an account given a Region object, game name, and tag line."""
        url = f'https://{region.route}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id.name}/{riot_id.tag_line}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_account_by_riot_id(): {e}")
            return None

        account = None
        try:
            account = Account(response.json(), region)
        except Exception as e:
            print(f"Error in get_account_by_riot_id(): {e}")
            return None
        return account


    # ----- Summoner functions
    def get_summoner_by_name(self, region, name):
        """Obtain a summoner given a Region object and name. Returns a Summoner object.
        Don't use this, outdated"""
        url = f'https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in getSummonerByName(): {e}")
            return None

        summoner = None
        try:
            summoner = Summoner(response.json(), region)
        except Exception as e:
            print(f"Error in get_summoner_by_name(): {e}")
            return None
        return summoner


    def get_summoner_by_account(self, region: Region, account: Account):
        """Obtain a summoner given a Region object and name. This uses the summoners/by-puuid endpoint using a puuid,
        this simply gives an additional option for getting a summoner. This method is not recommended."""
        url = f'https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{account.puuid}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_summoner_by_account(): {e}")
            return None

        summoner = None
        try:
            summoner = Summoner(response.json(), region)
        except Exception as e:
            print(f"Error in get_summoner_by_account(): {e}")
            return None
        return summoner


    def get_summoner_by_puuid(self, region: Region, puuid: str) -> Optional[Summoner]:
        """Obtain a summoner given a Region object and a puuid."""
        url = f"https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.riot_key}"
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_summoner_by_puuid(): {e}")
            return None

        summoner = None
        try:
            summoner = Summoner(response.json(), region)
        except Exception as e:
            print(f"Error in get_summoner_by_puuid(): {e}")
            return None
        return summoner


    def get_summoner_by_summoner_id(self, region: Region, summ_id: str) -> Optional[Summoner]:
        url = f"https://{region.region}.api.riotgames.com/lol/summoner/v4/summoners/{summ_id}?api_key={self.riot_key}"
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_summoner_by_puuid(): {e}")
            return None

        summoner = None
        try:
            summoner = Summoner(response.json(), region)
        except Exception as e:
            print(f"Error in get_summoner_by_summoner_id(): {e}")
            return None
        return summoner


    def get_league_entry_by_summoner_id(self, region, summ_id) -> Optional[List[LeagueEntry]]:
        """Obtain a summoner's rank information given a region and name. Returns a list of LeagueEntry objects."""
        url = f'https://{region.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summ_id}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_league_entry_by_summoner_id(): {e}")
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
            print("------------------------- done getting matches")
        except RiotRateLimit as e:
            print(f"Error in getMatchesFromList(): {e}")


    async def async_get_match(self, region, match_id):
        """Helper function for getMatchesFromList().
        Returns a match's data as a json object given its match id."""
        url = f'https://{region.route}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.riot_key}'
        async with self.second_limiter:
            num = random.randint(1, 1000)
            print("function", num)
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                try:
                    self.validate_status_code(response.status_code)
                    print("done", num)
                    return response.json()
                except RiotAPIException as e:
                    print(f"Error in getMatch(): {e}")
                    return None


    def get_match_id_list_by_puuid(self, region, puuid, num_matches) -> Optional[List[str]]:
        """Obtain a given number of matchIds for a specified puuid. Returns a list of matchIds."""
        url = f'https://{region.route}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num_matches}&api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_match_id_list_by_puuid(): {e}")
            return None
        return list(response.json())


    def get_match_by_match_id(self, region_obj, match_id)  -> Optional[Match]:
        """Obtain match data given a region and matchId. Returns a Match json object."""
        url = f'https://{region_obj.route}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_account_by_riot_id(): {e}")
            return None
        try:
            match = Match(response.json())
        except Exception as e:
            print(f"Error in get_match_by_match_id(): {e}")
            return None
        return match


    # ----- Clash functions
    def get_tournaments(self, region) -> Optional[List[Tournament]]:
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


    def get_players_by_summoner_id(self, region_obj, summ_id) -> Optional[List[Player]]:
        """Returns a list of active Clash players for a given summoner ID. If a summoner registers for multiple
        tournaments at the same time (e.g. Saturday and Sunday) then both registrations would appear in the list."""
        url = f'https://{region_obj.region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{summ_id}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_players_by_summoner_id(): {e}")
            return None
        players = []
        for obj in response.json():
            player = Player(obj, obj['teamId'])
            players.append(player)
        return players


    def get_team_ids_by_summoner_id(self, region_obj, summ_id) -> Optional[List[str]]:
        """Obtain team ids given a region and summoner name. Returns a list of team_ids."""
        url = f'https://{region_obj.region}.api.riotgames.com/lol/clash/v1/players/by-summoner/{summ_id}?api_key={self.riot_key}'
        response = requests.get(url)
        try:
            self.validate_status_code(response.status_code)
        except RiotAPIException as e:
            print(f"Error in get_account_by_riot_id(): {e}")
            return None
        team_ids = []
        for obj in response.json():
            team_ids.append(obj['teamId'])
        return team_ids


    def get_team_by_team_id(self, region, team_id) -> Optional[Team]:
        """Obtain team information given a region and teamId. Returns a Team object."""
        url = f'https://{region.region}.api.riotgames.com/lol/clash/v1/teams/{team_id}?api_key={self.riot_key}'
        response = requests.get(url)
        if response.status_code != 200:  # Check if request was not successful
            print(f'Error in getTeamByTeamId(): {response.status_code}, {response.reason}')
            return None
        return Team(response.json())
