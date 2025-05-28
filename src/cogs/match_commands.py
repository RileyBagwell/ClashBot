import discord
from discord.ext import commands
from typing import Optional
from src.league.Account import Account
from src.league.Region import Region
from src.league.RiotID import RiotID
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.EmbedBuilder import EmbedBuilder
from src.utils.RiotRequestHandler import RiotRequestHandler

class MatchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Use shared resources from the bot instance
        self.req_handler = bot.req_handler
        self.db_handler = bot.db_handler
        self.em_builder = bot.em_builder
        self.logger = bot.logger

    @commands.command(name="matches", description="Return a list of recent match ids.")
    async def cmd_matches(self, ctx, region_str: str, riot_id_str: str, num_matches: str):
        """Sends a list of a given number of match ids from a given player."""
        try:
            # Log command invocation
            self.logger.info(f"Matches command invoked by {ctx.author} for {riot_id_str} in {region_str}")
            
            # Input validation
            try:
                num_matches = int(num_matches)
                if num_matches <= 0 or num_matches > 100:
                    await ctx.send("Please enter a number between 1 and 100 for the number of matches.")
                    return
            except ValueError:
                await ctx.send("Please enter a valid number for the number of matches.")
                return

            # Parse region and riot ID
            region = Region(region_str)
            if not region.is_valid:
                await ctx.send(f"Invalid region: {region_str}. Please use a valid region code.")
                return

            riot_id = RiotID(riot_id_str)
            if not riot_id.is_valid:
                await ctx.send(f"Invalid Riot ID format: {riot_id_str}. Please use the format 'name#tag'.")
                return
            
            # Get the account info
            account = await self.get_account(ctx, region, riot_id=riot_id)
            if account is None:
                self.logger.warning(f"Could not find account for {riot_id_str} in {region_str}")
                return
                
            # Get match history
            self.logger.debug(f"Fetching {num_matches} matches for {account.name_tag}")
            match_ids = self.req_handler.get_match_id_list_by_puuid(region, account.puuid, num_matches)
            
            if not match_ids:
                await ctx.send("No matches found for this player.")
                self.logger.info(f"No matches found for {account.name_tag}")
                return
                
            # Format and send response
            matches_str = "\n".join(match_ids)
            await ctx.send(f"Recent matches for {account.name_tag}:\n```{matches_str}```")
            self.logger.info(f"Successfully retrieved {len(match_ids)} matches for {account.name_tag}")
            
        except Exception as e:
            error_msg = f"An error occurred while processing the matches command: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            await ctx.send("Sorry, an error occurred while processing your request. Please try again later.")

    @cmd_matches.error
    async def matches_error(self, ctx, error):
        """Error handler for the matches command."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}. "
                         f"Usage: {self.bot.command_prefix}matches [region] [riot_id] [number_of_matches]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input and try again.")
        else:
            self.logger.error(f"Unexpected error in matches command: {str(error)}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please try again later.")

    @commands.command(name="match", description="Return information about a match given a match id.")
    async def cmd_match(self, ctx, region_str: str, match_id: str):
        """Display detailed information about a specific match."""
        try:
            # Log command invocation
            self.logger.info(f"Match command invoked by {ctx.author} for match {match_id} in {region_str}")

            # Parse region
            region = Region(region_str)
            if not region.is_valid:
                await ctx.send(f"Invalid region: {region_str}. Please use a valid region code.")
                return

            # Try to get match from database first
            self.logger.debug(f"Attempting to fetch match {match_id} from database")
            match_data = self.db_handler.get_match_by_match_id(match_id)
            
            # If not in database, fetch from API
            if not match_data:
                self.logger.debug(f"Match {match_id} not found in database, fetching from API")
                match_data = self.req_handler.get_match_by_match_id(region, match_id)
                if match_data:
                    self.logger.debug(f"Storing match {match_id} in database")
                    self.db_handler.add_matches([match_data])
            
            if not match_data:
                await ctx.send(f"Match {match_id} not found!")
                self.logger.warning(f"Match {match_id} not found in database or API")
                return
                
            # Build and send embed with match information
            self.logger.debug(f"Building embed for match {match_id}")
            embed = self.em_builder.build_embed_match(ctx, match_data)
            await ctx.send(embed=embed)
            self.logger.info(f"Successfully retrieved and displayed match {match_id}")

        except Exception as e:
            error_msg = f"An error occurred while processing the match command: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            await ctx.send("Sorry, an error occurred while processing your request. Please try again later.")

    @cmd_match.error
    async def match_error(self, ctx, error):
        """Error handler for the match command."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}. "
                         f"Usage: {self.bot.command_prefix}match [region] [match_id]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input and try again.")
        else:
            self.logger.error(f"Unexpected error in match command: {str(error)}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please try again later.")

    @commands.command(name="update", description="Update the database to show new matches.")
    async def cmd_update(self, ctx, region_str: str, riot_id_str: str):
        """Updates the database with recent matches from the given user and their team members."""
        try:
            # Log command invocation
            self.logger.info(f"Update command invoked by {ctx.author} for {riot_id_str} in {region_str}")

            # Parse region and riot ID
            region = Region(region_str)
            if not region.is_valid:
                await ctx.send(f"Invalid region: {region_str}. Please use a valid region code.")
                return

            riot_id = RiotID(riot_id_str)
            if not riot_id.is_valid:
                await ctx.send(f"Invalid Riot ID format: {riot_id_str}. Please use the format 'name#tag'.")
                return
            
            # Get account and summoner info
            account = await self.get_account(ctx, region, riot_id=riot_id)
            if account is None:
                self.logger.warning(f"Could not find account for {riot_id_str} in {region_str}")
                return

            message = await ctx.send(f"Updating matches for {account.name_tag}...")
            
            # Get recent matches
            self.logger.debug(f"Fetching recent matches for {account.name_tag}")
            match_id_list = self.req_handler.get_match_id_list_by_puuid(region, account.puuid, 25)
            matches_to_add = self.db_handler.validate_matches(match_id_list)
            
            if not matches_to_add:
                await message.edit(content=f"No new matches found for {account.name_tag}")
                self.logger.info(f"No new matches found for {account.name_tag}")
                return
            
            # Fetch and store new matches
            self.logger.debug(f"Found {len(matches_to_add)} new matches to add")
            match_list = []
            await self.req_handler.get_matches_from_list(region, matches_to_add, match_list)
            match_list = list(filter(lambda x: x is not None, match_list))
            
            if match_list:
                self.db_handler.add_matches(match_list)
                self.logger.info(f"Added {len(match_list)} new matches to database for {account.name_tag}")
                await message.edit(content=f'Added {len(match_list)} new matches to database for {account.name_tag}!')
            else:
                await message.edit(content=f"Failed to fetch new matches for {account.name_tag}")
                self.logger.warning(f"Failed to fetch new matches for {account.name_tag}")

        except Exception as e:
            error_msg = f"An error occurred while processing the update command: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            await ctx.send("Sorry, an error occurred while processing your request. Please try again later.")

    @cmd_update.error
    async def update_error(self, ctx, error):
        """Error handler for the update command."""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}. "
                         f"Usage: {self.bot.command_prefix}update [region] [riot_id]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided. Please check your input and try again.")
        else:
            self.logger.error(f"Unexpected error in update command: {str(error)}", exc_info=True)
            await ctx.send("An unexpected error occurred. Please try again later.")

    async def get_account(self, ctx, region: Region, riot_id=None) -> Optional[Account]:
        """Helper method to get account information."""
        try:
            if riot_id is not None and riot_id.is_valid:
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

async def setup(bot):
    await bot.add_cog(MatchCommands(bot)) 