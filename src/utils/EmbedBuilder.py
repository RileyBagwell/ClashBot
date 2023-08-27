import discord

from src.utils.DDragonRequestHandler import DDragonRequestHandler


class EmbedBuilder:
    def __init__(self):
        pass


    def buildSummonerEmbed(self, ctx, regionObj, summoner, leagueEntry):
        """Returns an embed for a given summoner."""
        dHandler = DDragonRequestHandler()
        iconURL = dHandler.getProfileIconURL(summoner.profileIconId)
        ranks = self.extractRanks(leagueEntry)
        embed = discord.Embed(
            title=summoner.name,
            colour=0x4a5691
        )
        embed.set_thumbnail(url=iconURL)
        embed.add_field(name="Summoner Level", value=summoner.summonerLevel, inline=False)
        embed.add_field(name="Solo/Duo Rank", value=ranks[0], inline=True)
        if leagueEntry[0] != 0:
            embed.add_field(name="Winrate", value=str(leagueEntry[0].winrate()) + f"% ({leagueEntry[0].totalGames()} games)", inline=True)
        else:
            embed.add_field(name="Winrate", value="0% (Unranked)", inline=True)
        embed.add_field(name="", value="", inline=False)  # Move to next line
        embed.add_field(name="Flex Rank", value=ranks[1], inline=True)
        if leagueEntry[1] != 0:
            embed.add_field(name="Winrate", value=str(leagueEntry[1].winrate()) + f"% ({leagueEntry[1].totalGames()} games)", inline=True)
        else:
            embed.add_field(name="Winrate", value="0% (Unranked)", inline=True)
        embed.add_field(name="", value=f"[u.gg Profile](https://u.gg/lol/profile/{regionObj.region}/{summoner.name.replace(' ', '')}/overview)",
                        inline=False)
        return embed


    def extractRanks(self, leagueEntry):
        """Extract the ranked information for a leagueEntry. Returns an array with ranks.
            Helper method for buildSummonerEmbed."""
        ranks = [0] * 2
        entry0 = leagueEntry[0]
        entry1 = leagueEntry[1]
        if entry0 != 0:
            ranks[0] = entry0.tier.title() + ' ' + entry0.rank
        else:
            ranks[0] = 'Unranked'
        if entry1 != 0:
            ranks[1] = entry1.tier.title() + ' ' + entry1.rank
        else:
            ranks[1] = 'Unranked'
        return ranks
