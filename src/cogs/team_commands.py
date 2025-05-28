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

class TeamCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Use shared resources from the bot instance
        self.req_handler = bot.req_handler
        self.db_handler = bot.db_handler
        self.em_builder = bot.em_builder
        self.logger = bot.logger

    @commands.command(name="team", description="Look up a team given a player's name")
    async def cmd_team(self, ctx, region_str: str, riot_id_str: str):
        """Look up and display information about a team based on a player's Riot ID."""
        try:
            # Log command invocation
            self.logger.info(f"Team command invoked by {ctx.author} for {riot_id_str} in {region_str}")
            
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

            # Get team information
            self.logger.debug(f"Fetching team info for {account.name_tag}")
            team_data = self.req_handler.get_team_by_summoner_id(region, summoner.id)
            if not team_data:
                await ctx.send(f"No team found for {account.name_tag}")
                self.logger.info(f"No team found for {account.name_tag}")
                return

            # Build and send team embed
            self.logger.debug(f"Building team embed for {account.name_tag}'s team")
            embed = self.em_builder.build_embed_team(ctx, region, team_data)
            await ctx.send(embed=embed)
            self.logger.info(f"Successfully displayed team info for {account.name_tag}")

        except Exception as e:
            error_msg = f"An error occurred while processing the team command: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            await ctx.send("Sorry, an error occurred while processing your request. Please try again later.")

    @cmd_team.error
    async def team_error(self, ctx, error):
        """Error handler for the team command."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}. "
                         f"Usage: {self.bot.command_prefix}team [region] [riot_id]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input and try again.")
        else:
            self.logger.error(f"Unexpected error in team command: {str(error)}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please try again later.")

    @commands.command(name="tournaments", description="Return all active or upcoming tournaments.")
    async def cmd_tournaments(self, ctx, region_str: str):
        """Display information about active or upcoming tournaments in the specified region."""
        try:
            # Log command invocation
            self.logger.info(f"Tournaments command invoked by {ctx.author} for region {region_str}")

            # Parse region
            region = Region(region_str)
            if not region.is_valid:
                await ctx.send(f"Invalid region: {region_str}. Please use a valid region code.")
                return

            # Get tournament data
            self.logger.debug(f"Fetching tournament data for region {region_str}")
            tournaments = self.req_handler.get_active_tournaments(region)
            if not tournaments:
                await ctx.send(f"No active tournaments found in {region_str}!")
                self.logger.info(f"No active tournaments found in {region_str}")
                return

            # Build and send tournament embed
            self.logger.debug(f"Building tournament embed for {len(tournaments)} tournaments")
            embed = self.em_builder.build_embed_tournaments(ctx, region, tournaments)
            await ctx.send(embed=embed)
            self.logger.info(f"Successfully displayed tournament info for {region_str}")

        except Exception as e:
            error_msg = f"An error occurred while processing the tournaments command: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            await ctx.send("Sorry, an error occurred while processing your request. Please try again later.")

    @cmd_tournaments.error
    async def tournaments_error(self, ctx, error):
        """Error handler for the tournaments command."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}. "
                         f"Usage: {self.bot.command_prefix}tournaments [region]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input and try again.")
        else:
            self.logger.error(f"Unexpected error in tournaments command: {str(error)}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please try again later.")

    async def get_account(self, ctx, region: Region, riot_id=None) -> Optional[Account]:
        """Helper method to get account information."""
        try:
            if riot_id is not None and riot_id.is_valid:
                self.logger.debug(f"Getting account by Riot ID: {riot_id}")
                account = self.req_handler.get_account_by_riot_id(region, riot_id)
                if account is None:
                    await ctx.send(f'Account *{riot_id}* in region *{region.region}* not found!')
                return account
            else:
                await ctx.send("Please enter a valid Riot ID!")
                return None
        except Exception as e:
            self.logger.error(f"Error getting account information: {str(e)}", exc_info=True)
            await ctx.send("An error occurred while fetching account information.")
            return None

    async def get_summoner(self, ctx, region: Region, puuid=None) -> Optional[Summoner]:
        """Helper method to get summoner information."""
        try:
            if puuid is not None:
                self.logger.debug(f"Getting summoner by PUUID: {puuid}")
                summoner = self.req_handler.get_summoner_by_puuid(region, puuid)
                if summoner is None:
                    await ctx.send(f'Summoner not found in region *{region.region}*!')
                return summoner
            else:
                await ctx.send("An error occurred while fetching summoner information.")
                return None
        except Exception as e:
            self.logger.error(f"Error getting summoner information: {str(e)}", exc_info=True)
            await ctx.send("An error occurred while fetching summoner information.")
            return None

async def setup(bot):
    await bot.add_cog(TeamCommands(bot)) 