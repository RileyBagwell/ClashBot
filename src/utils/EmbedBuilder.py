import datetime
import json
from typing import Optional
import os
from pathlib import Path

import discord

from src.utils.DDragonRequestHandler import DDragonRequestHandler


class EmbedBuilder:
    def __init__(self):
        """Initializes game_modes, game_types, maps, and queues as lists of dictionaries from the files."""
        file_path = Path(__file__).parent.parent / 'league' / 'files'
        self.game_modes = json.load(open(file_path / 'gameModes.json'))
        self.game_types = json.load(open(file_path / 'gameTypes.json'))
        self.maps = json.load(open(file_path / 'maps.json'))
        self.queues = json.load(open(file_path / 'queues.json'))


    # ----- Helper Function
    def extract_ranks(self, league_entry):
        """Extract the ranked information for a leagueEntry. Returns an array with ranks.
            Helper method for buildSummonerEmbed."""
        ranks = [None, None]
        entry0 = league_entry[0]
        entry1 = league_entry[1]
        if entry0 is not None:
            ranks[0] = entry0.tier.title() + ' ' + entry0.rank
        else:
            ranks[0] = 'Unranked'
        if entry1 is not None:
            ranks[1] = entry1.tier.title() + ' ' + entry1.rank
        else:
            ranks[1] = 'Unranked'
        return ranks


    def parse_files(self, info_dict) -> dict:
        """Attempts to grab the description of a game mode, type, map, and queue from the files.
        Parameters:
            info_dict: dictionary containing game_mode, game_type, map, and queue keys with their respective
                values from the API.
        Returns:
            The same dictionary, with modified values to contain the correct descriptions from the files, or
                "Unknown" if it cannot be found."""
        try:  # game_modes
            for obj in self.game_modes:
                if obj['gameMode'] == info_dict['game_mode']:
                    info_dict['game_mode'] = obj['description']
        except Exception as e:
            print(f"Error in parse_files(); can't parse gameModes: {e}")
            info_dict['game_mode'] = "Unknown"

        try:  # game_types
            for obj in self.game_types:
                if obj['gametype'] == info_dict['game_type']:
                    info_dict['game_type'] = obj['description']
        except Exception as e:
            print(f"Error in parse_files(); can't parse gameTypes: {e}")
            info_dict['game_type'] = "Unknown"

        try:  # maps
            for obj in self.maps:
                if obj['mapId'] == info_dict['map']:
                    info_dict['mapId'] = obj['mapName']
        except Exception as e:
            print(f"Error in parse_files(); can't parse maps {e}")
            info_dict['map'] = "Unknown"

        try:  # queues
            for obj in self.game_modes:
                if obj['queueId'] == info_dict['queues']:
                    info_dict['queues'] = obj['description']
        except Exception as e:
            print(f"Error in parse_files(); can't parse queues: {e}")
            info_dict['queue'] = "Unknown"
        return info_dict


    # ----- Builder Functions
    def build_embed_summoner(self, ctx, region_obj, account, summoner, league_entries):
        """Returns an embed for a given summoner."""
        dd_handler = DDragonRequestHandler()
        icon_url = dd_handler.get_profile_icon_url(summoner.profile_icon_id)
        ranks = self.extract_ranks(league_entries)
        embed = discord.Embed(
            title=account.name,
            colour=0x4a5691
        )
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="Summoner Level", value=summoner.summoner_level, inline=False)
        # Solo/Duo
        embed.add_field(name="Solo/Duo Rank", value=ranks[0], inline=True)
        if league_entries[0] is not None:
            embed.add_field(name="Winrate", value=str(league_entries[0].winrate()) + f"% ({league_entries[0].total_games()} games)", inline=True)
        else:
            embed.add_field(name="Winrate", value="0% (Unranked)", inline=True)
        embed.add_field(name="", value="", inline=False)  # Move to next line
        # Flex
        embed.add_field(name="Flex Rank", value=ranks[1], inline=True)
        if league_entries[1] is not None:
            embed.add_field(name="Winrate", value=str(league_entries[1].winrate()) + f"% ({league_entries[1].total_games()} games)", inline=True)
        else:
            embed.add_field(name="Winrate", value="0% (Unranked)", inline=True)
        embed.add_field(name="", value=f"[u.gg Profile](https://u.gg/lol/profile/{region_obj.region}/{account.name.replace(' ', '')}/overview)",
                        inline=False)
        return embed


    def build_embed_match_generic(self, ctx, match):
        """Returns an embed for a given match."""
        try:
            time = datetime.datetime.utcfromtimestamp(match.game_start_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error in build_embed_match_generic(): {e}")
            time = "Error"
        embed = discord.Embed(
            title=f"Match {match.match_id}",
            colour=0x4a5691
        )


        #game_mode = self.game_modes[match.game_mode]
        print(match.game_mode)
        #embed.add_field(name="Game Mode", value=self.game_modes[match.game_mode], inline=True)
        embed.add_field(name="Game Type", value=match.game_type, inline=True)
        embed.add_field(name="Game Duration", value=match.game_duration, inline=True)
        embed.add_field(name="Game Version", value=match.game_version, inline=True)
        embed.add_field(name="Map ID", value=match.map_id, inline=True)
        embed.add_field(name="Queue ID", value=match.queue_id, inline=True)
        embed.add_field(name="Platform ID", value=match.platform_id, inline=True)
        embed.add_field(name="Game Start Timestamp", value=match.game_start_timestamp, inline=True)
        embed.add_field(name="Game End Timestamp", value=match.game_end_timestamp, inline=True)
        embed.add_field(name="Tournament Code", value=match.tournament_code, inline=True)
        embed.set_footer(text=f"{time} utc")
        return embed


    def build_embed_match(self, ctx, match):
        """Returns an embed for a given match."""
        try:
            time = datetime.datetime.utcfromtimestamp(match.game_start_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error in build_embed_match(): {e}")
            time = "Error"

        embed = discord.Embed(
            title=f"Match {match.match_id}",
            colour=0x4a5691
        )

        # Game Info
        embed.add_field(name="Game Mode", value=match.game_mode, inline=True)
        embed.add_field(name="Game Type", value=match.game_type, inline=True)
        embed.add_field(name="Duration", value=f"{match.game_duration // 60}:{match.game_duration % 60:02d}", inline=True)

        # Map and Queue Info
        for obj in self.maps:
            if obj['mapId'] == match.map_id:
                map_name = obj['mapName']
                break
        else:
            map_name = f"Map {match.map_id}"

        for obj in self.queues:
            if obj['queueId'] == match.queue_id:
                queue_name = obj['description']
                break
        else:
            queue_name = f"Queue {match.queue_id}"

        embed.add_field(name="Map", value=map_name, inline=True)
        embed.add_field(name="Queue", value=queue_name, inline=True)
        embed.add_field(name="Version", value=match.game_version, inline=True)

        # Participants
        if hasattr(match, 'participants'):
            # Team 1
            team1_text = ""
            team2_text = ""
            for p in match.participants:
                player_name = p.summoner_name if p.summoner_name else p.riot_id_game_name if p.riot_id_game_name else "Unknown"
                kda_text = f"**{player_name}** ({p.champion_name}): {p.kills}/{p.deaths}/{p.assists}\n"
                if p.team_id == 100:  # Blue team
                    team1_text += kda_text
                else:  # Red team
                    team2_text += kda_text
            
            if team1_text:
                embed.add_field(name="Blue Team", value=team1_text, inline=True)
            if team2_text:
                embed.add_field(name="Red Team", value=team2_text, inline=True)

        embed.set_footer(text=f"{time} UTC")
        return embed
