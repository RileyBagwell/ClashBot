import asyncio
import os
from dotenv import load_dotenv
import discord
from src.ClashBot import ClashBot

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Bot setup
prefix = '##'
intents = discord.Intents.default()
intents.message_content = True
bot = ClashBot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

if __name__ == "__main__":
    asyncio.run(bot.start(os.getenv('BOT_KEY')))
