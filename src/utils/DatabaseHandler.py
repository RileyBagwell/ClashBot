import json
import os
import time

from dotenv import load_dotenv

import mysql.connector
from mysql.connector import errorcode

from src.league.match.Match import Match
from src.league.match.Participant import Participant
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
        self.cnx = None
        try:
            self.cnx = self.connect_to_mysql()
        except Exception as e:
            print(f"Error in DatabaseHandler.__init__(): {e}")
            self.cnx = None


    def connect_to_mysql(self, attempts=3, delay=2):
        attempt = 1
        # Reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**self.config)
            except (mysql.connector.Error, IOError) as err:
                if attempts is attempt:  # Check if all attempts have been exhausted
                    print(f"Failed to connect, exiting without a connection: {err}")
                    return None
                print(f"Connection failed: {err}. Retrying ({attempt}/{attempts})...")
            finally:
                print("Connected to MySQL server.")
            time.sleep(delay ** attempt)
            attempt += 1  # Reconnect delay
        return None


    def add_matches(self, match_list):
        """Adds matches to the database given a list of match json objects."""
        try:
            print("Preparing to add matches to database...")
            cursor = self.cnx.cursor()
            print(f"Matches to add: {len(match_list)}")

            matches_added = 0

            # Add match information to database
            insert_match_sql = (
                "INSERT INTO matches (dataVersion, matchId, gameCreation, gameDuration, gameEndTimestamp, gameId,"
                "gameMode, gameName, gameStartTimestamp, gameType, gameVersion, mapId, platformId, queueId, tournamentCode) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            insert_participant_sql = (
                "INSERT INTO participants (matchId, allInPings, assistMePings, assists, baronKills, bountyLevel, champExperience, champLevel, championId, championName, championTransform,"
                "commandPings, consumablesPurchased, damageDealtToBuildings, damageDealtToObjectives, damageDealtToTurrets, damageSelfMitigated, dangerPings, deaths, detectorWardsPlaced,"
                "doubleKills, dragonKills, eligibleForProgression, enemyMissingPings, firstBloodAssist, firstBloodKill, firstTowerAssist, firstTowerKill, gameEndedInEarlySurrender, gameEndedInSurrender,"
                "getBackPings, goldEarned, goldSpent, holdPings, individualPosition, inhibitorKills, inhibitorTakedowns, inhibitorsLost, item0, item1, item2, item3, item4, item5, item6,"
                "itemsPurchased, killingSprees, kills, lane, largestCriticalStrike, largestKillingSpree, largestMultiKill, longestTimeSpentLiving, magicDamageDealt,"
                "magicDamageDealtToChampions, magicDamageTaken, needVisionPings, neutralMinionsKilled, nexusKills, nexusTakedowns, nexusLost, objectivesStolen, objectivesStolenAssists,"
                "onMyWayPings, participantId, pentaKills, perk_defense, perk_flex, perk_offense, physicalDamageDealt, physicalDamageDealtToChampions, physicalDamageTaken,"
                "placement, playerAugment1, playerAugment2, playerAugment3, playerAugment4, playerSubteamId, profileIcon, pushPings, puuid, quadraKills, riotIdGameName, riotIdTagLine, role, sightWardsBoughtInGame,"
                "spell1Casts, spell2Casts, spell3Casts, spell4Casts, summoner1Casts, summoner1Id, summoner2Casts, summoner2Id, summonerId, summonerLevel, summonerName, teamEarlySurrendered,"
                "teamId, teamPosition, timeCCingOthers, timePlayed, totalAllyJungleMinionsKilled, totalDamageDealt, totalDamageDealtToChampions, totalDamageShieldedOnTeammates, totalDamageTaken,"
                "totalEnemyJungleMinionsKilled, totalHeal, totalHealsOnTeammates, totalMinionsKilled, totalTimeCCDealt, totalTimeSpentDead, totalUnitsHealed, tripleKills, trueDamageDealt,"
                "trueDamageDealtToChampions, trueDamageTaken, turretKills, turretTakedowns, turretsLost, unrealKills, visionClearedPings, visionScore, visionWardsBoughtInGame, wardsKilled, wardsPlaced, win) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
                ",%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            insert_match_data = []
            insert_participant_data = []
            for match_data in match_list:
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
                        part['quadraKills'], part['riotIdGameName'], part['riotIdTagline'], part['role'],
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

            print("Adding matches to database...")
            cursor.executemany(insert_match_sql, insert_match_data)
            print("Adding participants to database...")
            cursor.executemany(insert_participant_sql, insert_participant_data)
            print(f"Matches added: {matches_added}")

            self.cnx.commit()  # Ensure data is committed
            cursor.close()
            self.cnx.close()
        except Exception as e:
            print(f"Error in addMatches(): {e}")
            self.cnx.rollback()
            cursor.close()
            self.cnx.close()


    def validate_matches(self, match_id_list):
        """Returns an updated list of matchIds that are not present in the database from a given list of matchIds."""
        connection = self.get_connection()
        cursor = connection.cursor()
        look_for = ', '.join([f"'{element}'" for element in match_id_list])
        db_id_list = []
        cursor.execute(f"SELECT matchId FROM matches WHERE matchId IN ({look_for});")
        db_id_list = [row[0] for row in cursor.fetchall()]
        connection.close()
        return list(set(match_id_list) - set(db_id_list))


    def update_summoners_matches(self, region_obj, puuid):
        """Given a summoner's region and puuid, checks if the database is up-to-date with all the summoner's matches.
            If all matches were checked, returns 1. Otherwise, returns 0."""
        connection = self.get_connection()
        cursor = connection.cursor()
        req_handler = RiotRequestHandler()
        match_id_list = req_handler.get_match_id_list_by_puuid(region_obj, puuid, 100)
        # Validate that matches were found
        if len(match_id_list) == 0:
            print("updateSummonerMatches(): No matches found from player.")
            return
        # Find matchIds that are not already in database
        look_for = ""
        for match_id in match_id_list:
            look_for += f"'{match_id}', "
        look_for = look_for[:-2]  # Remove trailing ', '
        cursor.execute(f"SELECT match_id FROM matches WHERE match_id IN ({look_for});")
        row = cursor.fetchall()
        matches_in_db = str(row)
        matches_to_add = []
        for match_id in match_id_list:
            if matches_in_db.find(match_id) == -1:
                matches_to_add.append(match_id)
        self.add_matches(region_obj, matches_to_add)
        return 1


    def get_match_by_match_id(self, match_id):
        """Returns a Match.py object from the database if it exists."""
        select_query_match = f"""SELECT * FROM matches WHERE matchId='{match_id}';"""
        select_query_participants = f"""SELECT * FROM participants WHERE matchId='{match_id}';"""
        with self.cnx.cursor() as cursor:
            cursor.execute(select_query_match)
            match_result = cursor.fetchall()
        match = Match()
        with self.cnx.cursor() as cursor:
            cursor.execute(select_query_participants)
            participant_result = cursor.fetchall()
        participants = []
        for row in participant_result:
            part = Participant(row)
            participants.append(part)
        return participants
