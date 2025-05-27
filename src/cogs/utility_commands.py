import discord
from discord.ext import commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = '##'  # Move this to a config file in the future

    @commands.command(name="ping", description="Have the bot respond with a pong.")
    async def cmd_ping(self, ctx):
        """Simple ping command to check if the bot is responsive."""
        await ctx.send('Pong!')

    @commands.command(name="commands", description="Display all commands and information.")
    async def cmd_commands(self, ctx):
        """Sends a list of commands and what they do."""
        commands_str = f"""**__Commands:__**
            **{self.prefix}commands**: Display this message
            **{self.prefix}summoner [region] [riot id]**: Get a summoner's information given their Riot ID
            **{self.prefix}team [region] [riot id]**: Get a team given a summoner's Riot ID
            **{self.prefix}tournaments [region]**: Show active or upcoming tournaments for a given region
            **{self.prefix}matches [region] [name] [numMatches]**: Get a list of a summoner's match ids
            **{self.prefix}match [region] [match_id]**: Get detailed information about a specific match
            **{self.prefix}update [region] [riot id]**: Update the database with recent matches"""
        await ctx.send(commands_str)

    @commands.command(name="help", description="Display information about and how to use the bot.")
    async def cmd_help(self, ctx):
        """Sends a message with information about the bot and how to use it."""
        help_str = f"""This bot is designed to help you look up opposing teams in League of Legends Clash tournaments.
For a list of commands, use the `{self.prefix}commands` command.

THIS BOT IS IN DEVELOPMENT. If you encounter any issues, please contact <@852050979867459594>.

Use `{self.prefix}team [region] [riot id]` to look up a team by a player's Riot ID. This will give
you a basic profile view of each player, as well as a link to their u.gg profile."""
        await ctx.send(help_str)

async def setup(bot):
    await bot.add_cog(UtilityCommands(bot)) 