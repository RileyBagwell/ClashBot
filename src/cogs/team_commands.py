import discord
from discord.ext import commands
from typing import Optional
from src.league.Region import Region
from src.league.RiotID import RiotID
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

    @commands.command(name="team", description="Look up a team given a player's name")
    async def cmd_team(self, ctx, region_str, riot_id_str):
        """Look up and display information about a team based on a player's Riot ID."""
        region = Region(region_str)
        riot_id = RiotID(riot_id_str)
        
        # Get account and summoner info
        account = await self.get_account(ctx, region, riot_id=riot_id)
        if account is None:
            return
        summoner = await self.get_summoner(ctx, region, puuid=account.puuid)
        if summoner is None:
            return

        # Get team information
        team_data = self.req_handler.get_team_by_summoner_id(region, summoner.id)
        if not team_data:
            await ctx.send(f"No team found for {account.name_tag}")
            return

        # Build and send team embed
        embed = self.em_builder.build_embed_team(ctx, region, team_data)
        await ctx.send(embed=embed)

    @commands.command(name="tournaments", description="Return all active or upcoming tournaments.")
    async def cmd_tournaments(self, ctx, region):
        """Display information about active or upcoming tournaments in the specified region."""
        region_obj = Region(region)
        if not region_obj.is_valid:
            await ctx.send("Please choose a valid region!")
            return

        # Get tournament data
        tournaments = self.req_handler.get_active_tournaments(region_obj)
        if not tournaments:
            await ctx.send(f"No active tournaments found in {region}!")
            return

        # Build and send tournament embed
        embed = self.em_builder.build_embed_tournaments(ctx, region_obj, tournaments)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TeamCommands(bot)) 