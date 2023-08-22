import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

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
bot_token = os.getenv('BOT_KEY')


def verifyRegion(region):
    """Returns true if the given region is valid. Otherwise, returns false. Call this after correctRegion()."""
    regions = {'br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru', 'ph2', 'sg2', 'th2', 'tw2', 'vn2'}
    region = region.lower()
    if region in regions:
        return True
    return False


def correctRegion(region):
    """Attempt to correct a given region to work with API. i.e. 'na' -> 'na1'"""
    region = region.lower()
    if region == 'na':
        return 'na1'
    if region == 'br':
        return 'br1'
    if region == 'lan':
        return 'la1'
    if region == 'las':
        return 'la2'
    if region == 'eune':
        return 'eun1'
    if region == 'euw':
        return 'euw1'
    if region == "tr":
        return 'tr1'
    if region == 'jp':
        return 'jp1'
    if region == 'oce':
        return 'oc1'
    return region


async def validateSummoner(ctx, region, name):
    """Validates that a summoner exists, and if not, sends a message that it does not exist. Returns the summoner, or
        None if the summoner does not exist."""
    region = correctRegion(region)
    if verifyRegion(region) is False:
        await ctx.send("Please choose a valid region!")
        return None
    summoner = reqHandler.getSummonerByName(region, name)
    if summoner is None:
        await ctx.send(f'Summoner *{name}* in region *{region}* not found!')
        return None
    return summoner


@bot.command()
async def test(ctx):
    print('test triggered')
    obj = reqHandler.getLeagueEntryBySummonerId('na1', 'Blockerw1z')
    await ctx.send(obj[0].leagueId)


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
    region = correctRegion(region)
    summoner = await validateSummoner(ctx, region, name)
    if summoner is not None:
        leagueEntry = reqHandler.getLeagueEntryBySummonerId(region, summoner.id)
        emBuilder = EmbedBuilder()
        embed = emBuilder.buildSummonerEmbed(ctx, region, summoner, leagueEntry)
        await ctx.send(content="", embed=embed)
    return


@bot.command(name="matches", description="Return a list of recent match ids.")
async def cmd_matches(ctx, region, name, numMatches):
    """Sends a list of a given number of match ids from a given player."""
    # Check for a valid number of matches
    if int(numMatches) < 1 or int(numMatches) > 100:
        await ctx.send("Please enter a number between 1 and 100 (inclusive)!")
        return
    # Check for a valid region
    region = correctRegion(region)
    if verifyRegion(region) is False:
        await ctx.send("Please choose a valid region!")
        return

    # Request summoner for puuid
    puuid = reqHandler.getPuuidByName(region, name)
    if puuid is None:
        await ctx.send(f'Summoner *{name}* in region *{region}* not found!')
        return
    matches = reqHandler.getMatchesByPuuid(region, puuid, numMatches)
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
    summoner = await validateSummoner(ctx, region, name)
    region = correctRegion(region)
    if summoner is None:  # Exit function if summoner is not found, error messages already sent
        return
    teamIds = reqHandler.getTeamIdsBySummonerId(region, summoner.id)  # Obtain teamIds
    if len(teamIds) == 0:  # Check if summoner is in a team
        await ctx.send(f'Summoner {summoner.name} is not currently in a clash team.')
        return
    team = reqHandler.getTeamByTeamId(region, teamIds[0])  # Get the soonest team's information
    for player in team.players:
        tempSumm = reqHandler.getSummonerById(region, player.summonerId)
        leagueEntry = reqHandler.getLeagueEntryBySummonerId(region, player.summoner.id)
        emBuilder = EmbedBuilder()
        embed = emBuilder.buildSummonerEmbed(ctx, region, tempSumm, leagueEntry)
        await ctx.send(content="", embed=embed)


@bot.command(name="tournaments", description="Return all active or upcoming tournaments.")
async def cmd_tournaments(ctx, region):
    """Sends all active or upcoming tournaments given a region."""
    region = correctRegion(region)
    if verifyRegion(region) is False:
        await ctx.send("Please choose a valid region!")
        return
    tournaments = reqHandler.getTournaments(region)
    if len(tournaments) == 0:
        await ctx.send("No upcoming tournaments.")
    str = ''
    for obj in tournaments:
        str += obj.nameKey + ' '
    await ctx.send(str)


@bot.event
async def on_ready():
    """Triggers when the bot is logged in and ready for commands. Does any start-up functions."""
    print(f'We have logged in as {bot.user}')


# Run the bot with the specified token
bot.run(bot_token)
