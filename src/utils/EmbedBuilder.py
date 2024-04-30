import datetime
import json
from typing import Optional

import discord

from src.utils.DDragonRequestHandler import DDragonRequestHandler


class EmbedBuilder:
    def __init__(self):
        file_path = '../src/league/files/'
        self.game_modes = json.load(open(file_path+'gameModes.json'))
        self.game_types = json.load(open(file_path+'gameTypes.json'))
        self.maps = json.load(open(file_path+'maps.json'))
        self.queues = json.load(open(file_path+'queues.json'))


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


    def parse_files(self) -> Optional[list[str]]:
        pass


    # ----- Builder Functions
    def build_embed_summoner(self, ctx, region_obj, summoner, league_entry):
        """Returns an embed for a given summoner."""
        dd_handler = DDragonRequestHandler()
        icon_url = dd_handler.get_profile_icon_url(summoner.profile_icon_id)
        ranks = self.extract_ranks(league_entry)
        embed = discord.Embed(
            title=summoner.name,
            colour=0x4a5691
        )
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="Summoner Level", value=summoner.summoner_level, inline=False)
        embed.add_field(name="Solo/Duo Rank", value=ranks[0], inline=True)
        if league_entry[0] is not None:
            embed.add_field(name="Winrate", value=str(league_entry[0].winrate()) + f"% ({league_entry[0].total_games()} games)", inline=True)
        else:
            embed.add_field(name="Winrate", value="0% (Unranked)", inline=True)
        embed.add_field(name="", value="", inline=False)  # Move to next line
        embed.add_field(name="Flex Rank", value=ranks[1], inline=True)
        if league_entry[1] is not None:
            embed.add_field(name="Winrate", value=str(league_entry[1].winrate()) + f"% ({league_entry[1].total_games()} games)", inline=True)
        else:
            embed.add_field(name="Winrate", value="0% (Unranked)", inline=True)
        embed.add_field(name="", value=f"[u.gg Profile](https://u.gg/lol/profile/{region_obj.region}/{summoner.name.replace(' ', '')}/overview)",
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
        game_mode = "Unknown"
        game_type = "Unknown"
        map = "Unknown"
        queue = "Unknown"

        game_mode = self.game_modes[match.game_mode]
        print(match.game_mode)
        embed.add_field(name="Game Mode", value=self.game_modes[match.game_mode], inline=True)
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
