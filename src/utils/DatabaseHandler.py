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
        else:
            print("Connected to database.")



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
                "INSERT INTO matches (dataVersion, matchId, endOfGameResult, gameCreation, gameDuration, gameEndTimestamp, gameId,"
                "gameMode, gameName, gameStartTimestamp, gameType, gameVersion, mapId, platformId, queueId, tournamentCode) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            insert_team_sql = (
                "INSERT INTO teams (matchId, teamId, win) VALUES (%s, %s, %s)")

            insert_ban_sql = (
                "INSERT INTO bans (matchId, teamId, championId, pickTurn) VALUES (%s, %s, %s, %s)")

            insert_objective_sql = (
                "INSERT INTO objectives (matchId, teamId, objectiveType, first, kills) VALUES (%s, %s, %s, %s, %s)")

            insert_participant_sql = (
                "INSERT INTO participants (matchId, allInPings, assistMePings, assists, baronKills, bountyLevel, champExperience, champLevel, championId, championName, championTransform,"
                "commandPings, consumablesPurchased, damageDealtToBuildings, damageDealtToObjectives, damageDealtToTurrets, damageSelfMitigated, dangerPings, deaths, detectorWardsPlaced,"
                "doubleKills, dragonKills, eligibleForProgression, enemyMissingPings, enemyVisionPings, firstBloodAssist, firstBloodKill, firstTowerAssist, firstTowerKill, gameEndedInEarlySurrender, gameEndedInSurrender,"
                "getBackPings, goldEarned, goldSpent, holdPings, individualPosition, inhibitorKills, inhibitorTakedowns, inhibitorsLost, item0, item1, item2, item3, item4, item5, item6,"
                "itemsPurchased, killingSprees, kills, lane, largestCriticalStrike, largestKillingSpree, largestMultiKill, longestTimeSpentLiving, magicDamageDealt,"
                "magicDamageDealtToChampions, magicDamageTaken, needVisionPings, neutralMinionsKilled, nexusKills, nexusTakedowns, nexusLost, objectivesStolen, objectivesStolenAssists,"
                "onMyWayPings, participantId, pentaKills, physicalDamageDealt, physicalDamageDealtToChampions, physicalDamageTaken,"
                "placement, playerAugment1, playerAugment2, playerAugment3, playerAugment4, playerSubteamId, profileIcon, pushPings, puuid, quadraKills, riotIdGameName, riotIdTagLine, role, sightWardsBoughtInGame,"
                "spell1Casts, spell2Casts, spell3Casts, spell4Casts, summoner1Casts, summoner1Id, summoner2Casts, summoner2Id, summonerId, summonerLevel, summonerName, teamEarlySurrendered,"
                "teamId, teamPosition, timeCCingOthers, timePlayed, totalAllyJungleMinionsKilled, totalDamageDealt, totalDamageDealtToChampions, totalDamageShieldedOnTeammates, totalDamageTaken,"
                "totalEnemyJungleMinionsKilled, totalHeal, totalHealsOnTeammates, totalMinionsKilled, totalTimeCCDealt, totalTimeSpentDead, totalUnitsHealed, tripleKills, trueDamageDealt,"
                "trueDamageDealtToChampions, trueDamageTaken, turretKills, turretTakedowns, turretsLost, unrealKills, visionClearedPings, visionScore, visionWardsBoughtInGame, wardsKilled, wardsPlaced, win, subteamPlacement) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
                ",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

            insert_match_data = []
            insert_team_data = []
            insert_ban_data = []
            insert_objective_data = []
            insert_participant_data = []

            for match_data in match_list:
                if match_data is None:
                    continue
                matches_added += 1
                
                # Handle both dictionary and Match object formats
                if isinstance(match_data, dict):
                    metadata = match_data['metadata']
                    info = match_data['info']
                    match_tuple = (
                        metadata['dataVersion'], metadata['matchId'], info.get('endOfGameResult'), info['gameCreation'],
                        info['gameDuration'], info['gameEndTimestamp'], info['gameId'], info['gameMode'],
                        info['gameName'], info['gameStartTimestamp'], info['gameType'], info['gameVersion'],
                        info['mapId'], info['platformId'], info['queueId'], info['tournamentCode']
                    )
                    teams = info.get('teams', [])
                    participants = info.get('participants', [])
                else:  # Match object
                    match_tuple = (
                        match_data.data_version, match_data.match_id, match_data.end_of_game_result,
                        match_data.game_creation, match_data.game_duration, match_data.game_end_timestamp,
                        match_data.game_id, match_data.game_mode, match_data.game_name,
                        match_data.game_start_timestamp, match_data.game_type, match_data.game_version,
                        match_data.map_id, match_data.platform_id, match_data.queue_id, match_data.tournament_code
                    )
                    teams = match_data.teams
                    participants = match_data.participants

                insert_match_data.append(match_tuple)
                match_id = match_tuple[1]  # matchId is the second field

                # Process teams, bans, and objectives
                for team in teams:
                    team_id = team['teamId'] if isinstance(team, dict) else team.team_id
                    win = team['win'] if isinstance(team, dict) else team.win
                    insert_team_data.append((match_id, team_id, win))

                    # Process bans
                    bans = team['bans'] if isinstance(team, dict) else team.bans
                    for ban in bans:
                        champion_id = ban['championId'] if isinstance(ban, dict) else ban.championId
                        pick_turn = ban['pickTurn'] if isinstance(ban, dict) else ban.pickTurn
                        insert_ban_data.append((match_id, team_id, champion_id, pick_turn))

                    # Process objectives
                    objectives = team['objectives'] if isinstance(team, dict) else team.objectives
                    if objectives:
                        for obj_type, obj_data in (objectives.items() if isinstance(objectives, dict) else vars(objectives).items()):
                            first = obj_data['first'] if isinstance(obj_data, dict) else obj_data.first
                            kills = obj_data['kills'] if isinstance(obj_data, dict) else obj_data.kills
                            insert_objective_data.append((match_id, team_id, obj_type, first, kills))

                # Process participants
                for part in participants:
                    if isinstance(part, dict):
                        # Handle dictionary format
                        participant_tuple = self._create_participant_tuple_from_dict(match_id, part)
                    else:
                        # Handle Participant object format
                        participant_tuple = self._create_participant_tuple_from_object(match_id, part)
                    insert_participant_data.append(participant_tuple)

            # Execute all inserts
            print("Adding matches to database...")
            cursor.executemany(insert_match_sql, insert_match_data)
            
            print("Adding teams to database...")
            cursor.executemany(insert_team_sql, insert_team_data)
            
            print("Adding bans to database...")
            cursor.executemany(insert_ban_sql, insert_ban_data)
            
            print("Adding objectives to database...")
            cursor.executemany(insert_objective_sql, insert_objective_data)
            
            print("Adding participants to database...")
            cursor.executemany(insert_participant_sql, insert_participant_data)
            
            print(f"Matches added: {matches_added}")

            self.cnx.commit()  # Ensure data is committed
            cursor.close()

        except Exception as e:
            print(f"Error in addMatches(): {e}")
            self.cnx.rollback()
            cursor.close()

    def _create_participant_tuple_from_dict(self, match_id, part):
        """Helper method to create participant tuple from dictionary data."""
        return (
            match_id, part['allInPings'], part['assistMePings'], part['assists'],
            part['baronKills'], part['bountyLevel'], part['champExperience'],
            part['champLevel'], part['championId'], part['championName'],
            part['championTransform'], part['commandPings'], part['consumablesPurchased'],
            part['damageDealtToBuildings'], part['damageDealtToObjectives'], part['damageDealtToTurrets'],
            part['damageSelfMitigated'], part['dangerPings'], part['deaths'], part['detectorWardsPlaced'],
            part['doubleKills'], part['dragonKills'], part['eligibleForProgression'], part['enemyMissingPings'],
            part['enemyVisionPings'], part['firstBloodAssist'], part['firstBloodKill'], part['firstTowerAssist'],
            part['firstTowerKill'], part['gameEndedInEarlySurrender'], part['gameEndedInSurrender'],
            part['getBackPings'], part['goldEarned'], part['goldSpent'], part['holdPings'], part['individualPosition'],
            part['inhibitorKills'], part['inhibitorTakedowns'], part['inhibitorsLost'], part['item0'], part['item1'],
            part['item2'], part['item3'], part['item4'], part['item5'], part['item6'], part['itemsPurchased'],
            part['killingSprees'], part['kills'], part['lane'], part['largestCriticalStrike'], part['largestKillingSpree'],
            part['largestMultiKill'], part['longestTimeSpentLiving'], part['magicDamageDealt'],
            part['magicDamageDealtToChampions'], part['magicDamageTaken'], part['needVisionPings'],
            part['neutralMinionsKilled'], part['nexusKills'], part['nexusTakedowns'], part['nexusLost'],
            part['objectivesStolen'], part['objectivesStolenAssists'], part['onMyWayPings'], part['participantId'],
            part['pentaKills'], part['physicalDamageDealt'], part['physicalDamageDealtToChampions'],
            part['physicalDamageTaken'], part['placement'], part['playerAugment1'], part['playerAugment2'],
            part['playerAugment3'], part['playerAugment4'], part['playerSubteamId'], part['profileIcon'],
            part['pushPings'], part['puuid'], part['quadraKills'], part['riotIdGameName'], part['riotIdTagline'],
            part['role'], part['sightWardsBoughtInGame'], part['spell1Casts'], part['spell2Casts'],
            part['spell3Casts'], part['spell4Casts'], part['summoner1Casts'], part['summoner1Id'],
            part['summoner2Casts'], part['summoner2Id'], part['summonerId'], part['summonerLevel'],
            part['summonerName'], part['teamEarlySurrendered'], part['teamId'], part['teamPosition'],
            part['timeCCingOthers'], part['timePlayed'], part['totalAllyJungleMinionsKilled'],
            part['totalDamageDealt'], part['totalDamageDealtToChampions'], part['totalDamageShieldedOnTeammates'],
            part['totalDamageTaken'], part['totalEnemyJungleMinionsKilled'], part['totalHeal'],
            part['totalHealsOnTeammates'], part['totalMinionsKilled'], part['totalTimeCCDealt'],
            part['totalTimeSpentDead'], part['totalUnitsHealed'], part['tripleKills'], part['trueDamageDealt'],
            part['trueDamageDealtToChampions'], part['trueDamageTaken'], part['turretKills'], part['turretTakedowns'],
            part['turretsLost'], part['unrealKills'], part['visionClearedPings'], part['visionScore'],
            part['visionWardsBoughtInGame'], part['wardsKilled'], part['wardsPlaced'], part['win'],
            part.get('subteamPlacement', 0)
        )

    def _create_participant_tuple_from_object(self, match_id, part):
        """Helper method to create participant tuple from Participant object."""
        return (
            match_id, part.all_in_pings, part.assist_me_pings, part.assists,
            part.baron_kills, part.bounty_level, part.champ_experience,
            part.champ_level, part.champion_id, part.champion_name,
            part.champion_transform, part.command_pings, part.consumables_purchased,
            part.damage_dealt_to_buildings, part.damage_dealt_to_objectives, part.damage_dealt_to_turrets,
            part.damage_self_mitigated, part.danger_pings, part.deaths, part.detector_wards_placed,
            part.double_kills, part.dragon_kills, part.eligible_for_progression, part.enemy_missing_pings,
            part.enemy_vision_pings, part.first_blood_assist, part.first_blood_kill, part.first_tower_assist,
            part.first_tower_kill, part.game_ended_in_early_surrender, part.game_ended_in_surrender,
            part.get_back_pings, part.gold_earned, part.gold_spent, part.hold_pings, part.individual_position,
            part.inhibitor_kills, part.inhibitor_takedowns, part.inhibitors_lost, part.item0, part.item1,
            part.item2, part.item3, part.item4, part.item5, part.item6, part.items_purchased,
            part.killing_sprees, part.kills, part.lane, part.largest_critical_strike, part.largest_killing_spree,
            part.largest_multi_kill, part.longest_time_spent_living, part.magic_damage_dealt,
            part.magic_damage_dealt_to_champions, part.magic_damage_taken, part.need_vision_pings,
            part.neutral_minions_killed, part.nexus_kills, part.nexus_takedowns, part.nexus_lost,
            part.objectives_stolen, part.objectives_stolen_assists, part.on_my_way_pings, part.participant_id,
            part.penta_kills, part.physical_damage_dealt, part.physical_damage_dealt_to_champions,
            part.physical_damage_taken, part.placement, part.player_augment1, part.player_augment2,
            part.player_augment3, part.player_augment4, part.player_subteam_id, part.profile_icon,
            part.push_pings, part.puuid, part.quadra_kills, part.riot_id_game_name, part.riot_id_tagline,
            part.role, part.sight_wards_bought_in_game, part.spell1_casts, part.spell2_casts,
            part.spell3_casts, part.spell4_casts, part.summoner1_casts, part.summoner1_id,
            part.summoner2_casts, part.summoner2_id, part.summoner_id, part.summoner_level,
            part.summoner_name, part.team_early_surrendered, part.team_id, part.team_position,
            part.time_ccing_others, part.time_played, part.total_ally_jungle_minions_killed,
            part.total_damage_dealt, part.total_damage_dealt_to_champions, part.total_damage_shielded_on_teammates,
            part.total_damage_taken, part.total_enemy_jungle_minions_killed, part.total_heal,
            part.total_heals_on_teammates, part.total_minions_killed, part.total_time_ccdealt,
            part.total_time_spent_dead, part.total_units_healed, part.triple_kills, part.true_damage_dealt,
            part.true_damage_dealt_to_champions, part.true_damage_taken, part.turret_kills, part.turret_takedowns,
            part.turrets_lost, part.unreal_kills, part.vision_cleared_pings, part.vision_score,
            part.vision_wards_bought_in_game, part.wards_killed, part.wards_placed, part.win,
            part.subteam_placement
        )


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
            if not match_result:
                return None
            match = Match(match_result[0])  # Pass the tuple to Match constructor
            
            cursor.execute(select_query_participants)
            participant_result = cursor.fetchall()
            participants = []
            for row in participant_result:
                # Create a new tuple with match_id as the first element
                participant_tuple = (match_id,) + row[1:]  # Skip the first element of row since it's match_id
                part = Participant(participant_tuple)
                participants.append(part)
            
            match.participants = participants
            return match
