import discord
from discord.ext import commands
from typing import Optional
from src.league.Region import Region
from src.league.RiotID import RiotID
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.EmbedBuilder import EmbedBuilder
from src.utils.RiotRequestHandler import RiotRequestHandler

class MatchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.req_handler = RiotRequestHandler()
        self.db_handler = DatabaseHandler()
        self.em_builder = EmbedBuilder()

    @commands.command(name="matches", description="Return a list of recent match ids.")
    async def cmd_matches(self, ctx, region_str, riot_id_str, num_matches):
        """Sends a list of a given number of match ids from a given player."""
        region = Region(region_str)
        riot_id = RiotID(riot_id_str)
        
        # Get the account and summoner info
        account = await self.get_account(ctx, region, riot_id=riot_id)
        if account is None:
            return
            
        # Get match history
        match_ids = self.req_handler.get_match_id_list_by_puuid(region, account.puuid, int(num_matches))
        if not match_ids:
            await ctx.send("No matches found for this player.")
            return
            
        # Format and send response
        matches_str = "\n".join(match_ids)
        await ctx.send(f"Recent matches for {account.name_tag}:\n```{matches_str}```")

    @commands.command(name="match", description="Return information about a match given a match id.")
    async def cmd_match(self, ctx, region_str, match_id):
        """Display detailed information about a specific match."""
        region = Region(region_str)
        if not region.is_valid:
            await ctx.send("Please choose a valid region!")
            return

        # Try to get match from database first
        match_data = self.db_handler.get_match_by_match_id(match_id)
        
        # If not in database, fetch from API
        if not match_data:
            match_data = self.req_handler.get_match_by_match_id(region, match_id)
            if match_data:
                self.db_handler.add_matches([match_data])
        
        if not match_data:
            await ctx.send(f"Match {match_id} not found!")
            return
            
        # Build and send embed with match information
        embed = self.em_builder.build_embed_match(ctx, match_data)
        await ctx.send(embed=embed)

    @commands.command(name="update", description="Update the database to show new matches.")
    async def cmd_update(self, ctx, region_str, riot_id_str):
        """Updates the database with recent matches from the given user and their team members."""
        region = Region(region_str)
        riot_id = RiotID(riot_id_str)
        
        # Get account and summoner info
        account = await self.get_account(ctx, region, riot_id=riot_id)
        if account is None:
            return
        summoner = await self.get_summoner(ctx, region, puuid=account.puuid)
        if summoner is None:
            return

        message = await ctx.send(f"Updating matches for {account.name_tag}...")
        
        # Get recent matches
        match_id_list = self.req_handler.get_match_id_list_by_puuid(region, summoner.puuid, 25)
        matches_to_add = self.db_handler.validate_matches(match_id_list)
        
        # Fetch and store new matches
        match_list = []
        await self.req_handler.get_matches_from_list(region, matches_to_add, match_list)
        match_list = list(filter(lambda x: x is not None, match_list))
        self.db_handler.add_matches(match_list)
        
        await message.edit(content='Database has been updated with your most recent matches!')

async def setup(bot):
    await bot.add_cog(MatchCommands(bot)) 