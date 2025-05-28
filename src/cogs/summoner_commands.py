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
        self.logger = bot.logger

    @commands.command(name="summoner", description="Pull up information of a summoner.")
    async def cmd_summoner(self, ctx, region_str: str, riot_id_str: str):
        """Sends an embed with a basic profile view of a given summoner."""
        try:
            # Log command invocation
            self.logger.info(f"Summoner command invoked by {ctx.author} for {riot_id_str} in {region_str}")

            # Parse region and riot ID
            region = Region(region_str)
            if not region.is_valid:
                await ctx.send(f"Invalid region: {region_str}. Please use a valid region code.")
                return

            riot_id = RiotID(riot_id_str)
            if not riot_id.is_valid:
                await ctx.send(f"Invalid Riot ID format: {riot_id_str}. Please use the format 'name#tag'.")
                return

            # Get account info
            self.logger.debug(f"Fetching account info for {riot_id_str}")
            account = await self.get_account(ctx, region, riot_id=riot_id)
            if account is None:
                self.logger.warning(f"Could not find account for {riot_id_str} in {region_str}")
                return

            # Get summoner info
            self.logger.debug(f"Fetching summoner info for {account.name_tag}")
            summoner = await self.get_summoner(ctx, region, puuid=account.puuid)
            if summoner is None:
                self.logger.warning(f"Could not find summoner info for {account.name_tag}")
                return

            # Get league entries
            self.logger.debug(f"Fetching league entries for {account.name_tag}")
            league_entries = self.req_handler.get_league_entry_by_summoner_id(region, summoner.id)
            
            # Build and send embed
            self.logger.debug(f"Building embed for {account.name_tag}")
            embed = self.em_builder.build_embed_summoner(ctx, region, account, summoner, league_entries)
            await ctx.send(content="", embed=embed)
            self.logger.info(f"Successfully displayed summoner info for {account.name_tag}")

        except Exception as e:
            error_msg = f"An error occurred while processing the summoner command: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            await ctx.send("Sorry, an error occurred while processing your request. Please try again later.")

    @cmd_summoner.error
    async def summoner_error(self, ctx, error):
        """Error handler for the summoner command."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}. "
                         f"Usage: {self.bot.command_prefix}summoner [region] [riot_id]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input and try again.")
        else:
            self.logger.error(f"Unexpected error in summoner command: {str(error)}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please try again later.")

    async def get_summoner(self, ctx, region: Region, account=None, puuid=None, summ_id=None) -> Optional[Summoner]:
        """Obtains a summoner from the API and deserializes it, and returns it as a Summoner object. Validates that the
        region is valid.
        """
        try:
            if not region.is_valid:  # Validate region
                await ctx.send("Please choose a valid region!")
                return None

            summoner = None
            if account is not None:  # Get summoner by account object
                self.logger.debug(f"Getting summoner by account: {account.name_tag}")
                summoner = self.req_handler.get_summoner_by_account(region, account)
            elif puuid is not None:  # Get summoner by puuid
                self.logger.debug(f"Getting summoner by PUUID: {puuid}")
                summoner = self.req_handler.get_summoner_by_puuid(region, puuid)
            elif summ_id is not None:  # Get summoner by summoner id
                self.logger.debug(f"Getting summoner by summoner ID: {summ_id}")
                summoner = self.req_handler.get_summoner_by_summoner_id(region, summ_id)
            else:
                self.logger.error("No valid parameter provided to get_summoner")
                await ctx.send("An error occurred while fetching summoner information.")
                return None

            if summoner is None:
                await ctx.send(f'Summoner *{account.name_tag if account else ""}* in region *{region.region}* not found!')
                return None
            return summoner

        except Exception as e:
            self.logger.error(f"Error getting summoner information: {str(e)}", exc_info=True)
            await ctx.send("An error occurred while fetching summoner information.")
            return None

    async def get_account(self, ctx, region: Region, puuid=None, riot_id=None) -> Optional[Account]:
        """Obtains an account from the API and deserializes it, and returns it as an Account object."""
        try:
            if not region.is_valid:  # Validate region
                await ctx.send("Please choose a valid region!")
                return None

            account = None
            if puuid is not None:  # Get account by puuid
                self.logger.debug(f"Getting account by PUUID: {puuid}")
                account = self.req_handler.get_account_by_puuid(region, puuid)
            elif riot_id is not None:  # Get account by riot id
                if riot_id.is_valid:  # Validate riot id
                    self.logger.debug(f"Getting account by Riot ID: {riot_id}")
                    account = self.req_handler.get_account_by_riot_id(region, riot_id)
                else:
                    await ctx.send("Please enter a valid Riot ID!")
                    return None
            else:
                self.logger.error("No valid parameter provided to get_account")
                await ctx.send("An error occurred while fetching account information.")
                return None

            if account is None:  # Check if account exists
                await ctx.send(f'Account *{riot_id}* in region *{region.region}* not found!')
                return None
            return account

        except Exception as e:
            self.logger.error(f"Error getting account information: {str(e)}", exc_info=True)
            await ctx.send("An error occurred while fetching account information.")
            return None

async def setup(bot):
    await bot.add_cog(SummonerCommands(bot)) 