import discord
from discord.ext import commands
from typing import Optional
from src.league.Account import Account
from src.league.Region import Region
from src.league.RiotID import RiotID
from src.league.Summoner import Summoner
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.EmbedBuilder import EmbedBuilder
from src.utils.RiotRequestHandler import RiotRequestHandler

class SummonerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Use shared resources from the bot instance
        self.req_handler = bot.req_handler
        self.db_handler = bot.db_handler
        self.em_builder = bot.em_builder

    async def get_summoner(self, ctx, region: Region, account=None, puuid=None, summ_id=None) -> Optional[Summoner]:
        """Obtains a summoner from the API and deserializes it, and returns it as a Summoner object. Validates that the
        region is valid.
        """
        if not region.is_valid:  # Validate region
            await ctx.send("Please choose a valid region!")
            return None

        summoner = None
        if account is not None:  # Get summoner by account object
            summoner = self.req_handler.get_summoner_by_account(region, account)
        elif puuid is not None:  # Get summoner by puuid
            summoner = self.req_handler.get_summoner_by_puuid(region, puuid)
        elif summ_id is not None:  # Get summoner by summoner id
            summoner = self.req_handler.get_summoner_by_summoner_id(region, summ_id)
        else:
            print("Error in get_summoner(): You must specify an api endpoint parameter.")

        if summoner is None:
            await ctx.send(f'Summoner *{account.name_tag if account else ""}* in region *{region.region}* not found!')
            return None
        return summoner

    async def get_account(self, ctx, region: Region, puuid=None, riot_id=None) -> Optional[Account]:
        """Obtains an account from the API and deserializes it, and returns it as an Account object."""
        if not region.is_valid:  # Validate region
            await ctx.send("Please choose a valid region!")
            return None

        account = None
        if puuid is not None:  # Get account by puuid
            account = self.req_handler.get_account_by_puuid(region, puuid)
        elif riot_id is not None:  # Get account by riot id
            if riot_id.is_valid:  # Validate riot id
                account = self.req_handler.get_account_by_riot_id(region, riot_id)
            else:
                await ctx.send("Please enter a valid Riot ID!")
                return None
        else:
            print("Error in get_account(): You must specify an api endpoint parameter.")

        if account is None:  # Check if account exists
            await ctx.send(f'Account *{riot_id}* in region *{region.region}* not found!')
            return None
        return account

    @commands.command(name="summoner", description="Pull up information of a summoner.")
    async def cmd_summoner(self, ctx, region_str, riot_id_str):
        """Sends an embed with a basic profile view of a given summoner."""
        region = Region(region_str)
        riot_id = RiotID(riot_id_str)
        account = await self.get_account(ctx, region, riot_id=riot_id)
        if account is None:
            return
        summoner = await self.get_summoner(ctx, region, puuid=account.puuid)
        if summoner is None:
            return
        league_entries = self.req_handler.get_league_entry_by_summoner_id(region, summoner.id)
        embed = self.em_builder.build_embed_summoner(ctx, region, account, summoner, league_entries)
        await ctx.send(content="", embed=embed)

async def setup(bot):
    await bot.add_cog(SummonerCommands(bot)) 