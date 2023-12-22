import discord

from src.utils.DDragonRequestHandler import DDragonRequestHandler


class EmbedBuilder:
    def __init__(self):
        pass


    def build_summoner_embed(self, ctx, region_obj, summoner, league_entry):
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
