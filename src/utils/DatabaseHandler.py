import json
import os
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import errorcode

from src.utils.RiotRequestHandler import RiotRequestHandler


class DatabaseHandler:
    def __init__(self):
        load_dotenv()  # Load .env file for database info
        # Configure database information
        self.config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_BASE')}


    def getConnection(self):
        """Attempts to connect to the MySQL server and returns a MySQLConnection object if successful."""
        try:
            connection = mysql.connector.connect(**self.config)  # Create connection with the server
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access denied, check permissions or username and password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print(err)
        else:
            return connection


    def addMatches(self, matchList):
        """Adds matches to the database given a list of match json objects."""
        connection = self.getConnection()
        cursor = connection.cursor()
        print(f"Matches to add: {len(matchList)}")
        matches_added = 0

        # Add match information to database
        insert_match_sql = (
            "INSERT INTO matches (dataVersion, matchId, gameCreation, gameDuration, gameEndTimestamp, gameId,"
            "gameMode, gameName, gameStartTimestamp, gameType, gameVersion, mapId, platformId, queueId, tournamentCode) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        insert_participant_sql = (
            "INSERT INTO participants (matchId, allInPings, assistMePings, assists, baronKills, baitPings, bountyLevel, champExperience, champLevel, championId, championName, championTransform,"
            "commandPings, consumablesPurchased, damageDealtToBuildings, damageDealtToObjectives, damageDealtToTurrets, damageSelfMitigated, dangerPings, deaths, detectorWardsPlaced,"
            "doubleKills, dragonKills, eligibleForProgression, enemyMissingPings, firstBloodAssist, firstBloodKill, firstTowerAssist, firstTowerKill, gameEndedInEarlySurrender, gameEndedInSurrender,"
            "getBackPings, goldEarned, goldSpent, holdPings, individualPosition, inhibitorKills, inhibitorTakedowns, inhibitorsLost, item0, item1, item2, item3, item4, item5, item6,"
            "itemsPurchased, killingSprees, kills, lane, largestCriticalStrike, largestKillingSpree, largestMultiKill, longestTimeSpentLiving, magicDamageDealt,"
            "magicDamageDealtToChampions, magicDamageTaken, needVisionPings, neutralMinionsKilled, nexusKills, nexusTakedowns, nexusLost, objectivesStolen, objectivesStolenAssists,"
            "onMyWayPings, participantId, pentaKills, perk_defense, perk_flex, perk_offense, physicalDamageDealt, physicalDamageDealtToChampions, physicalDamageTaken,"
            "placement, playerAugment1, playerAugment2, playerAugment3, playerAugment4, playerSubteamId, profileIcon, pushPings, puuid, quadraKills, riotIdName, riotIdTagLine, role, sightWardsBoughtInGame,"
            "spell1Casts, spell2Casts, spell3Casts, spell4Casts, summoner1Casts, summoner1Id, summoner2Casts, summoner2Id, summonerId, summonerLevel, summonerName, teamEarlySurrendered,"
            "teamId, teamPosition, timeCCingOthers, timePlayed, totalAllyJungleMinionsKilled, totalDamageDealt, totalDamageDealtToChampions, totalDamageShieldedOnTeammates, totalDamageTaken,"
            "totalEnemyJungleMinionsKilled, totalHeal, totalHealsOnTeammates, totalMinionsKilled, totalTimeCCDealt, totalTimeSpentDead, totalUnitsHealed, tripleKills, trueDamageDealt,"
            "trueDamageDealtToChampions, trueDamageTaken, turretKills, turretTakedowns, turretsLost, unrealKills, visionClearedPings, visionScore, visionWardsBoughtInGame, wardsKilled, wardsPlaced, win) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
            ",%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        insert_match_data = []
        insert_participant_data = []
        for match_data in matchList:
            if match_data is None:
                break
            matches_added += 1
            info = match_data['info']
            insert_match_data.append((match_data['metadata']['dataVersion'], match_data['metadata']['matchId'], info['gameCreation'], info['gameDuration'], info['gameEndTimestamp'],
                      info['gameId'], info['gameMode'], info['gameName'], info['gameStartTimestamp'], info['gameType'], info['gameVersion'],
                      info['mapId'], info['platformId'], info['queueId'], info['tournamentCode']))

            for part in info['participants']:
                insert_participant_data.append((
                    match_data['metadata']['matchId'], part['allInPings'], part['assistMePings'], part['assists'], part['baronKills'],
                    part['baitPings'],
                    part['bountyLevel'], part['champExperience'], part['champLevel'],
                    part['championId'], part['championName'], part['championTransform'], part['commandPings'],
                    part['consumablesPurchased'], part['damageDealtToBuildings'], part['damageDealtToObjectives'],
                    part['damageDealtToTurrets'], part['damageSelfMitigated'], part['dangerPings'], part['deaths'],
                    part['detectorWardsPlaced'], part['doubleKills'], part['dragonKills'],
                    part['eligibleForProgression'], part['enemyMissingPings'], part['firstBloodAssist'],
                    part['firstBloodKill'],
                    part['firstTowerAssist'], part['firstTowerKill'], part['gameEndedInEarlySurrender'],
                    part['gameEndedInSurrender'], part['getBackPings'], part['goldEarned'], part['goldSpent'],
                    part['holdPings'], part['individualPosition'], part['inhibitorKills'], part['inhibitorTakedowns'],
                    part['inhibitorsLost'], part['item0'], part['item1'], part['item2'], part['item3'], part['item4'],
                    part['item5'], part['item6'], part['itemsPurchased'], part['killingSprees'],
                    part['kills'], part['lane'], part['largestCriticalStrike'], part['largestKillingSpree'],
                    part['largestMultiKill'], part['longestTimeSpentLiving'], part['magicDamageDealt'],
                    part['magicDamageDealtToChampions'], part['magicDamageTaken'], part['needVisionPings'],
                    part['neutralMinionsKilled'],
                    part['nexusKills'], part['nexusTakedowns'], part['nexusLost'], part['objectivesStolen'],
                    part['objectivesStolenAssists'], part['onMyWayPings'], part['participantId'],
                    part['pentaKills'], part['perks']['statPerks']['defense'], part['perks']['statPerks']['flex'],
                    part['perks']['statPerks']['offense'],
                    part['physicalDamageDealt'], part['physicalDamageDealtToChampions'], part['physicalDamageTaken'],
                    part['placement'], part['playerAugment1'], part['playerAugment2'],
                    part['playerAugment3'], part['playerAugment4'], part['playerSubteamId'], part['profileIcon'],
                    part['pushPings'], part['puuid'],
                    part['quadraKills'], part['riotIdName'], part['riotIdTagline'], part['role'],
                    part['sightWardsBoughtInGame'], part['spell1Casts'], part['spell2Casts'],
                    part['spell3Casts'], part['spell4Casts'], part['summoner1Casts'], part['summoner1Id'],
                    part['summoner2Casts'], part['summoner2Id'],
                    part['summonerId'], part['summonerLevel'], part['summonerName'], part['teamEarlySurrendered'],
                    part['teamId'], part['teamPosition'],
                    part['timeCCingOthers'], part['timePlayed'], part['totalAllyJungleMinionsKilled'],
                    part['totalDamageDealt'],
                    part['totalDamageDealtToChampions'], part['totalDamageShieldedOnTeammates'],
                    part['totalDamageTaken'], part['totalEnemyJungleMinionsKilled'], part['totalHeal'],
                    part['totalHealsOnTeammates'], part['totalMinionsKilled'], part['totalTimeCCDealt'],
                    part['totalTimeSpentDead'],
                    part['totalUnitsHealed'], part['tripleKills'], part['trueDamageDealt'],
                    part['trueDamageDealtToChampions'],
                    part['trueDamageTaken'], part['turretKills'],
                    part['turretTakedowns'], part['turretsLost'], part['unrealKills'], part['visionClearedPings'],
                    part['visionScore'], part['visionWardsBoughtInGame'], part['wardsKilled'],
                    part['wardsPlaced'], part['win']))
        cursor.executemany(insert_match_sql, insert_match_data)
        cursor.executemany(insert_participant_sql, insert_participant_data)
        print(f"Matches added: {matches_added}")

        connection.commit()  # Ensure data is committed
        cursor.close()
        connection.close()


    def validateMatches(self, matchIdList):
        """Returns an updated list of matchIds that are not present in the database from a given list of matchIds."""
        connection = self.getConnection()
        cursor = connection.cursor()
        lookFor = ', '.join([f"'{element}'" for element in matchIdList])
        cursor.execute(f"SELECT matchId FROM matches WHERE matchId IN ({lookFor});")
        dbIdList = [row[0] for row in cursor.fetchall()]
        connection.close()
        return list(set(matchIdList) - set(dbIdList))


    def updateSummonersMatches(self, regionObj, puuid):
        """Given a summoner's region and puuid, checks if the database is up-to-date with all the summoner's matches.
            If all matches were checked, returns 1. Otherwise, returns 0."""
        connection = self.getConnection()
        cursor = connection.cursor()
        reqHandler = RiotRequestHandler()
        matchIdList = reqHandler.getMatchIdListByPuuid(regionObj, puuid, 100)
        # Validate that matches were found
        if len(matchIdList) == 0:
            print("updateSummonerMatches(): No matches found from player.")
            return
        # Find matchIds that are not already in database
        lookFor = ""
        for matchId in matchIdList:
            lookFor += f"'{matchId}', "
        lookFor = lookFor[:-2]  # Remove trailing ', '
        cursor.execute(f"SELECT matchId FROM matches WHERE matchId IN ({lookFor});")
        row = cursor.fetchall()
        matchesInDb = str(row)
        matchesToAdd = []
        for matchId in matchIdList:
            if matchesInDb.find(matchId) == -1:
                matchesToAdd.append(matchId)
        self.addMatches(regionObj, matchesToAdd)
        return 1


    def getMatchByMatchId(self, matchId, puuid):
        """Returns a Match object from the database if it exists."""
        connection = mysql.connector.connect(**self.config)
        select_query = f"""SELECT p.kills FROM Participant p JOIN Info i ON p.matchId = i.matchId WHERE p.puuid = '{puuid}' AND i.matchId = '{matchId}';"""
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            result = cursor.fetchall()
        for row in result:
            print(row)
        connection.close()


dbHandler = DatabaseHandler()
reqHandler = RiotRequestHandler()
#match = reqHandler.getMatchByMatchId('na1', 'NA1_4758776993')
#dbHandler.addMatch(match)
#match = reqHandler.getMatchByMatchId('na1', 'NA1_4754967858')
#dbHandler.addMatch(match)
