import asyncio
import os
import time
from typing import Optional

from dotenv import load_dotenv
import discord
from discord.ext import commands

from src.league.Account import Account
from src.league.Region import Region
from src.league.RiotID import RiotID
from src.league.Summoner import Summoner
from src.utils.DatabaseHandler import DatabaseHandler
from src.utils.EmbedBuilder import EmbedBuilder
from src.utils.RiotRequestHandler import RiotRequestHandler


# Define client and bot
prefix = '##'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Other set up tasks
load_dotenv()
req_handler = RiotRequestHandler()
db_handler = DatabaseHandler()
em_builder = EmbedBuilder()
bot_token = os.getenv('BOT_KEY')


async def get_summoner(ctx, region, account) -> Optional[Summoner]:
    """Obtains a summoner from the API and deserializes it, and returns it as a Summoner object. Validates that the
    region is valid.
    Args:
        ctx: The ctx of the message that called the function
        region: A region object of the region for the account to look up
        account: A account object of the account to look up
    Returns:
        Summoner object if summoner is found
        None if not found
    """
    if not region.is_valid:  # Validate region
        await ctx.send("Please choose a valid region!")
        return None
    summoner = req_handler.get_summoner_by_account(region, account)
    if summoner is None:
        await ctx.send(f'Summoner *{account.name_tag}* in region *{region.region}* not found!')
        return None
    return summoner


async def get_account(ctx, region, riot_id) -> Optional[Account]:
    """Obtains an account from the API and deserializes it, and returns it as an Account object. Validates that the
    region and riot_id are valid.
    Args:
        ctx: The ctx of the message that called the function
        region: A region object of the region for the account to look up
        riot_id: A RiotID object of the Riot ID to look up
    Returns:
        Account object if account is found
        None if not found
    """
    if not region.is_valid:  # Validate region
        await ctx.send("Please choose a valid region!")
        return None
    if not riot_id.is_valid:  # Validate riot_id
        await ctx.send("Please enter a valid Riot ID!")
        return None
    account = req_handler.get_account_by_riot_id(region, riot_id)
    if account is None:
        await ctx.send(f'Account *{riot_id}* in region *{region.region}* not found!')
        return None
    return account


@bot.command()
async def test(ctx):
    """Test command to quickly test the bot functionality."""
    message = await ctx.send("Doing first task...")
    time.sleep(2)
    await message.edit(content="Doing second task...")
    time.sleep(2)
    await message.edit(content="Done!")


@bot.command(name="update", description="Update the database to show new matches.")
async def cmd_update(ctx, region, name):
    """Updates the database if necessary for matches from the given user, and if they're in a team, their team members."""
    message = await ctx.send(f"Updating matches for {name} in {region}...")
    region_obj = Region(region)
    summoner = await get_summoner(ctx, region_obj, name)
    # Obtain match ids from the summoner
    match_id_list = req_handler.get_match_id_list_by_puuid(region_obj, summoner.puuid, 100)
    # Find which matches are not already in database
    matches_to_add = db_handler.validate_matches(match_id_list)
    match_list = []  # Empty list to store match data
    # Populate the match_list with match data from Riot API
    await req_handler.get_matches_from_list(region_obj, matches_to_add, match_list)
    match_list = list(filter(lambda x: x is not None, match_list))
    # Add the necessary matches to the database
    db_handler.add_matches(match_list)
    print("Done!")
    await message.edit(content='Database has been updated with your most recent matches!')


@bot.command(name="commands", description="Display all commands and information.")
async def cmd_commands(ctx):
    """Sends a list of commands and what they do."""
    str = f"""**__Commands:__**
**{prefix}commands**: Display this message
**{prefix}summoner [region] [name]**: Get a summoner's information
**{prefix}matches [region] [name] [numMatches]**: Get a list of a summoner's match ids
**{prefix}team [region] [name]**: Get a team given a summoner's name
**{prefix}tournaments [region]**: Get active or upcoming tournaments for a given region"""
    await ctx.send(str)


@bot.command(name="summoner", description="Pull up information of a summoner.")
async def cmd_summoner(ctx, region_str, riot_id_str):
    """Sends an embed with a basic profile view of a given summoner. Ctx is passed to necessary functions to edit
    the message upon failure.
    Command Args:
        region_str: The region of the summoner as a string
        riot_id_str: The Riot ID of the summoner as a string (Name#Tag)
    """
    region = Region(region_str)
    riot_id = RiotID(riot_id_str)
    account = await get_account(ctx, region, riot_id)  # Get account object
    if account is None:  # Verify the account was obtained
        return
    summoner = await get_summoner(ctx, region, account)
    if summoner is None:  # Verify the summoner was obtained
        return
    league_entry = req_handler.get_league_entry_by_summoner_id(region, summoner.id)
    embed = em_builder.build_embed_summoner(ctx, region, summoner, league_entry)
    await ctx.send(content="", embed=embed)
    return


@bot.command(name="matches", description="Return a list of recent match ids.")
async def cmd_matches(ctx, debug, region_str, riot_id_str, num_matches):
    """Sends a list of a given number of match ids from a given player.
    The debug flag is used to run the function with test data w/o a database interaction."""
    region = Region(region_str)
    riot_id = RiotID(riot_id_str)
    if int(num_matches) < 1 or int(num_matches) > 100:  # Check for a valid number of matches
        await ctx.send("Please enter a number between 1 and 100 (inclusive)!")
        return
    account = await get_account(ctx, region, riot_id)  # Get account object
    if account is None:  # Verify the account was obtained
        return
    # Logic:
    # Obtain list of matchIDs from RiotHandler
    # Use DBHandler to receive list of IDs NOT present in the database
    # If the list is not empty, request the match data with RRHandler
    # If the list is not empty, add the match data to DB with DBHandler
    # Use DBHandler to receive list of match data from the database
    # Send match data to EmbedBuilder
    await ctx.send("Command not fully implemented, but reached the end!")


@bot.command(name="match", description="Return information about a match given a match id.")
async def cmd_match(ctx, region_str, match_id):
    """Sends all information about a match given its id."""
    region = Region(region_str)
    if not region.is_valid:  # Validate region
        await ctx.send("Please choose a valid region!")
        return
    match = req_handler.get_match_by_match_id(region, match_id)
    try:
        embed = em_builder.build_embed_match_generic(ctx, match)
    except Exception as e:
        print(f"Error in cmd_match(): {e}")
        await ctx.send("An error occurred while processing the match data.")
        return
    await ctx.send(embed=embed, content=f"Command finished. {match.participants[0].summoner_name} vs {match.participants[5].summoner_name}")


@bot.command(name="team", description="Look up a team given a player's name")
async def cmd_team(ctx, region, name):
    """Sends information about a summoner's clash team given their region and name."""
    init_message = await ctx.send("Looking up player's team...")
    region_obj = Region(region)
    summoner = await get_summoner(ctx, region_obj, name)
    if summoner is None:  # Exit function if summoner is not found, error messages already sent
        return
    team_ids = req_handler.get_team_ids_by_summoner_id(region_obj, summoner.id)  # Obtain team_ids
    if len(team_ids) == 0:  # Check if summoner is not in a team
        await ctx.send(f'Summoner {summoner.name} is not currently in a clash team.')
        return
    team = req_handler.get_team_by_team_id(region_obj, team_ids[0])  # Get the soonest team's information
    await init_message.edit(content="Obtaining team's information...")
    for player in team.players:
        temp_summ = req_handler.get_summoner_by_id(region_obj, player.summoner_id)
        league_entry = req_handler.get_league_entry_by_summoner_id(region_obj, player.summoner_id)
        print(league_entry[0].total_games())
        embed = em_builder.build_embed_summoner(ctx, region_obj, temp_summ, league_entry)
        await ctx.send(content="", embed=embed)
    await init_message.edit("Team information displayed below.")


@bot.command(name="tournaments", description="Return all active or upcoming tournaments.")
async def cmd_tournaments(ctx, region):
    """Sends all active or upcoming tournaments given a region."""
    region_obj = Region(region)
    if region_obj.is_valid is False:
        await ctx.send("Please choose a valid region!")
        return
    tournaments = req_handler.get_tournaments(region_obj)
    if len(tournaments) == 0:
        await ctx.send("No upcoming tournaments.")
        return
    str = ''
    for obj in tournaments:
        str += obj.name_key + ' '
    await ctx.send(str)


@bot.event
async def on_ready():
    """Triggers when the bot is logged in and ready for commands. Does any start-up functions."""
    print(f'We have logged in as {bot.user}')


async def main():
    await bot.start(bot_token)


# Run the bot using asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())
