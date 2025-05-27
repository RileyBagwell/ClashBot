import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Bot setup
prefix = '##'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')  # Remove the default help command

# List of cogs to load
COGS = [
    'src.cogs.utility_commands',
    'src.cogs.summoner_commands',
    'src.cogs.match_commands',
    'src.cogs.team_commands'
]

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

async def load_extensions():
    """Load all cogs."""
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f'Loaded {cog}')
        except Exception as e:
            print(f'Failed to load {cog}: {str(e)}')

async def main():
    """Main function to start the bot."""
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('BOT_KEY'))

if __name__ == "__main__":
    asyncio.run(main())
