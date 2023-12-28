import asyncio
import os
import time

from dotenv import load_dotenv
import discord
from discord.ext import commands

from src.league.Region import Region
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


async def get_summoner(ctx, region_obj, name):
    """Obtains a summoner from the API. If it exists, returns the summoner as a Summoner object. If not, returns None
    and sends a message saying it was not found. 'region' parameter should be a Region object."""
    if region_obj.is_valid is False:
        await ctx.send("Please choose a valid region!")
        return None
    summoner = req_handler.get_summoner_by_name(region_obj, name)
    if summoner is None:
        await ctx.send(f'Summoner *{name}* in region *{region_obj.region}* not found!')
        return None
    return summoner


@bot.command()
async def test(ctx):
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
    # Add the necessary matches to the database
    db_handler.add_matches(match_list)
    await message.edit('Done updating!')


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
async def cmd_summoner(ctx, region, name):
    """Sends information for a summoner given a region and a name."""
    region_obj = Region(region)
    summoner = await get_summoner(ctx, region_obj, name)
    if summoner is not None:
        league_entry = req_handler.get_league_entry_by_summoner_id(region_obj, summoner.id)
        embed = em_builder.build_summoner_embed(ctx, region_obj, summoner, league_entry)
        await ctx.send(content="", embed=embed)
    return


@bot.command(name="matches", description="Return a list of recent match ids.")
async def cmd_matches(ctx, region, name, num_matches):
    """Sends a list of a given number of match ids from a given player."""
    # Check for a valid number of matches
    if int(num_matches) < 1 or int(num_matches) > 100:
        await ctx.send("Please enter a number between 1 and 100 (inclusive)!")
        return

    regionObj = Region(region)
    summoner = await get_summoner(ctx, regionObj, name)
    if summoner is None:
        return
    puuid = summoner.puuid
    matches = req_handler.get_match_id_list_by_puuid(regionObj, puuid, num_matches)
    if matches is None:
        await ctx.send(f'No matches found!')
        return
    str = "__Match Ids:__\n"
    for match_id in matches:
        str += match_id + ', '
    await ctx.send(str)


@bot.command(name="match", description="Return information about a match given a match id.")
async def cmd_match(ctx, matchId):
    """Sends all information about a match given its id."""
    await ctx.send("'match' command to be implemented")


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
        embed = em_builder.build_summoner_embed(ctx, region_obj, temp_summ, league_entry)
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
