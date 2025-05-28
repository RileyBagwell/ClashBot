import discord
from discord.ext import commands
import logging
import sys
from datetime import datetime
from pathlib import Path
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.EmbedBuilder import EmbedBuilder
from src.utils.RiotRequestHandler import RiotRequestHandler

class ClashBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.remove_command('help')  # Remove the default help command
        
        # Set up logging
        self.setup_logging()
        
        # Shared resources
        try:
            self.req_handler = RiotRequestHandler()
            self.db_handler = DatabaseHandler()
            self.em_builder = EmbedBuilder()
            self.logger.info("Successfully initialized bot resources")
        except Exception as e:
            self.logger.error(f"Failed to initialize bot resources: {str(e)}")
            raise

    def setup_logging(self):
        """Configure logging for the bot"""
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"clashbot_{timestamp}.log"
        
        # Configure logging
        self.logger = logging.getLogger('clashbot')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

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
                self.logger.info(f'Loaded {cog}')
            except Exception as e:
                self.logger.error(f'Failed to load {cog}: {str(e)}') 