import discord
from discord.ext import commands
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.EmbedBuilder import EmbedBuilder
from src.utils.RiotRequestHandler import RiotRequestHandler

class ClashBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.remove_command('help')  # Remove the default help command
        # Shared resources
        self.req_handler = RiotRequestHandler()
        self.db_handler = DatabaseHandler()
        self.em_builder = EmbedBuilder()

    async def setup_hook(self):
        """Called when the bot is starting up"""
        # List of cogs to load
        COGS = [
            'src.cogs.utility_commands',
            'src.cogs.summoner_commands',
            'src.cogs.match_commands',
            'src.cogs.team_commands'
        ]
        
        # Load all cogs
        for cog in COGS:
            try:
                await self.load_extension(cog)
                print(f'Loaded {cog}')
            except Exception as e:
                print(f'Failed to load {cog}: {str(e)}') 