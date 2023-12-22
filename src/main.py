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
reqHandler = RiotRequestHandler()
dbHandler = DatabaseHandler()
emBuilder = EmbedBuilder()
bot_token = os.getenv('BOT_KEY')


async def getSummoner(ctx, regionObj, name):
    """Obtains a summoner from the API. If it exists, returns the summoner as a Summoner object. If not, returns None
    and sends a message saying it was not found. 'region' parameter should be a Region object."""
    if regionObj.is_valid is False:
        await ctx.send("Please choose a valid region!")
        return None
    summoner = reqHandler.get_summoner_by_name(regionObj, name)
    if summoner is None:
        await ctx.send(f'Summoner *{name}* in region *{regionObj.region}* not found!')
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
    regionObj = Region(region)
    summoner = await getSummoner(ctx, regionObj, name)
    matchIdList = reqHandler.get_match_id_list_by_puuid(regionObj, summoner.puuid, 100)
    matchesToAdd = dbHandler.validate_matches(matchIdList)
    matchList = []  # Empty list to store match data
    await reqHandler.get_matches_from_list(regionObj, matchesToAdd, matchList)
    dbHandler.add_matches(matchList)
    await ctx.send('Done updating!')


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
    regionObj = Region(region)
    summoner = await getSummoner(ctx, regionObj, name)
    if summoner is not None:
        leagueEntry = reqHandler.get_league_entry_by_summoner_id(regionObj, summoner.id)
        emBuilder = EmbedBuilder()
        embed = emBuilder.build_summoner_embed(ctx, regionObj, summoner, leagueEntry)
        await ctx.send(content="", embed=embed)
    return


@bot.command(name="matches", description="Return a list of recent match ids.")
async def cmd_matches(ctx, region, name, numMatches):
    """Sends a list of a given number of match ids from a given player."""
    # Check for a valid number of matches
    if int(numMatches) < 1 or int(numMatches) > 100:
        await ctx.send("Please enter a number between 1 and 100 (inclusive)!")
        return

    regionObj = Region(region)
    summoner = await getSummoner(ctx, regionObj, name)
    if summoner is None:
        return
    puuid = summoner.puuid
    matches = reqHandler.get_match_id_list_by_puuid(regionObj, puuid, numMatches)
    if matches is None:
        await ctx.send(f'No matches found!')
        return
    str = "__Match Ids:__\n"
    for matchId in matches:
        str += matchId + ', '
    await ctx.send(str)


@bot.command(name="match", description="Return information about a match given a match id.")
async def cmd_match(ctx, matchId):
    """Sends all information about a match given its id."""
    await ctx.send("'match' command to be implemented")


@bot.command(name="team", description="Look up a team given a player's name")
async def cmd_team(ctx, region, name):
    """Sends information about a summoner's clash team given their region and name."""
    init_message = await ctx.send("Looking up player's team...")
    regionObj = Region(region)
    summoner = await getSummoner(ctx, regionObj, name)
    if summoner is None:  # Exit function if summoner is not found, error messages already sent
        return
    teamIds = reqHandler.get_team_ids_by_summoner_id(regionObj, summoner.id)  # Obtain teamIds
    if len(teamIds) == 0:  # Check if summoner is not in a team
        await ctx.send(f'Summoner {summoner.name} is not currently in a clash team.')
        return
    team = reqHandler.get_team_by_team_id(regionObj, teamIds[0])  # Get the soonest team's information
    await init_message.edit(content="Obtaining team's information...")
    for player in team.players:
        tempSumm = reqHandler.get_summoner_by_id(regionObj, player.summoner_id)
        leagueEntry = reqHandler.get_league_entry_by_summoner_id(regionObj, player.summoner_id)
        print(leagueEntry[0].total_games())
        embed = emBuilder.build_summoner_embed(ctx, regionObj, tempSumm, leagueEntry)
        await ctx.send(content="", embed=embed)
    await init_message.edit("Team information displayed below.")


@bot.command(name="tournaments", description="Return all active or upcoming tournaments.")
async def cmd_tournaments(ctx, region):
    """Sends all active or upcoming tournaments given a region."""
    regionObj = Region(region)
    if regionObj.is_valid is False:
        await ctx.send("Please choose a valid region!")
        return
    tournaments = reqHandler.get_tournaments(regionObj)
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
