import json
import os
from dotenv import load_dotenv

import mysql.connector

class DatabaseHandler:
    def __init__(self):
        self.config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'host': os.getenv('DV_HOST'),
            'database': os.getenv('DV_BASE')}
        connection = mysql.connector.connect(**self.config)
        """cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO test_users VALUES ('joe', '48')"
        )
        connection.commit()"""
        select_query = 'SELECT * FROM test_users'

        with connection.cursor() as cursor:
            cursor.execute(select_query)
            result = cursor.fetchall()

        for row in result:
            print(row)
        connection.close()


    def addMatch(self, MatchDto):
        """Adds a match to the database given it's MatchDto from the API."""
        connection = mysql.connector.connect(**self.config)
        match_data = json.loads(MatchDto)
        db_cursor = connection.cursor()

        metadata = match_data.get('metadata', {})
        db_cursor.execute(
            "INSERT INTO Metadata (matchId, dataVersion) VALUES (%s, %s)",
            (metadata.get("matchId"), metadata.get("dataVersion"))
        )
        connection.commit()


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


handler = DatabaseHandler()
handler.getMatchByMatchId('NA1_4746688295', 'oYMmFzmHEqn-LZnsw0XJEbb-o-_kMiBBJqIny9PGdoi0ZjzmIHtLJ8bOSO5IrbZrN50nn_f6xSBp4g')
str = """{
    "metadata": {
        "dataVersion": "2",
        "matchId": "NA1_4746688295",
        "participants": [
            "o-E_c-vUAu8__X42GHRySr7Cfe4hp9YC8QWPmsQ5dVG5mPFsWurXdBf_AE9qeASNJ5q1YpQxM6S98Q",
            "Vk1mQcXPtS3twf7WS4k8t3mkp07j2lM1BCRLCDx2Z-8VaVJO_j3r0TTJRjtsrJbXHkRgxaPW3X9teg",
            "iBZ9VD8a7x4wZfI5jwLjTeCgS4BU2vfb70SBmkexuh21JVd2Ois5HkIcm41C-SvMQr0plSM0gvf9Rg",
            "IashVvcF5Aef5xCXO6ThIIX9WmrMFT-cMJ6MO_yD6RnS9RtELWwiOQBJqQRKOPkFWiPwoGjU4Wt4aQ",
            "Dx6wZPz5BOo8wQhtE68kDxAfMf1iXDFIr0KmA7FRBMpfmpT8HzqfBOulL2vaYgL04HMPj_PbdpIx1w",
            "zM4adBKXIZXy1VX06J8P5hrtBhhPlFGOBHF1fc3I__Mb_c7qn2cVZUy4jfykuRCs7XFrrtuzCGXr6g",
            "oYMmFzmHEqn-LZnsw0XJEbb-o-_kMiBBJqIny9PGdoi0ZjzmIHtLJ8bOSO5IrbZrN50nn_f6xSBp4g",
            "MsNtGO8V4cCqzJKHnI5CvKXp2tX1avVl1LtrWdI7I_Od72iCVvt_gAp6drjc7AHFX2kSgTx1aEJN6Q"
        ]
    },
    "info": {
        "gameCreation": 1692078030026,
        "gameDuration": 961,
        "gameEndTimestamp": 1692079030083,
        "gameId": 4746688295,
        "gameMode": "CHERRY",
        "gameName": "teambuilder-match-4746688295",
        "gameStartTimestamp": 1692078068692,
        "gameType": "MATCHED_GAME",
        "gameVersion": "13.15.524.1760",
        "mapId": 30,
        "participants": [
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 6,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 17000,
                "champLevel": 18,
                "championId": 36,
                "championName": "DrMundo",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 6,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 46889,
                "dangerPings": 0,
                "deaths": 5,
                "detectorWardsPlaced": 0,
                "doubleKills": 1,
                "dragonKills": 0,
                "eligibleForProgression": true,
                "enemyMissingPings": 0,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 19800,
                "goldSpent": 24300,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 2049,
                "item1": 223107,
                "item2": 226667,
                "item3": 223065,
                "item4": 223047,
                "item5": 223222,
                "item6": 3348,
                "itemsPurchased": 14,
                "killingSprees": 2,
                "kills": 6,
                "lane": "NONE",
                "largestCriticalStrike": 0,
                "largestKillingSpree": 4,
                "largestMultiKill": 2,
                "longestTimeSpentLiving": 97,
                "magicDamageDealt": 20183,
                "magicDamageDealtToChampions": 15847,
                "magicDamageTaken": 37661,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 1,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 20332,
                "physicalDamageDealtToChampions": 9879,
                "physicalDamageTaken": 20617,
                "placement": 2,
                "playerAugment1": 71,
                "playerAugment2": 13,
                "playerAugment3": 15,
                "playerAugment4": 64,
                "playerSubteamId": 1,
                "profileIcon": 4075,
                "pushPings": 0,
                "puuid": "o-E_c-vUAu8__X42GHRySr7Cfe4hp9YC8QWPmsQ5dVG5mPFsWurXdBf_AE9qeASNJ5q1YpQxM6S98Q",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 87,
                "spell2Casts": 27,
                "spell3Casts": 43,
                "spell4Casts": 9,
                "subteamPlacement": 2,
                "summoner1Casts": 0,
                "summoner1Id": 2202,
                "summoner2Casts": 0,
                "summoner2Id": 2201,
                "summonerId": "KJ54R4CCwL2GOChNaS3PlzXDMpRdasTNzA-Pe_ki5ND0X2A",
                "summonerLevel": 208,
                "summonerName": "Gay Baby",
                "teamEarlySurrendered": false,
                "teamId": 100,
                "teamPosition": "",
                "timeCCingOthers": 19,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 40515,
                "totalDamageDealtToChampions": 25726,
                "totalDamageShieldedOnTeammates": 0,
                "totalDamageTaken": 60142,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 25713,
                "totalHealsOnTeammates": 4748,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 116,
                "totalTimeSpentDead": 1697,
                "totalUnitsHealed": 2,
                "tripleKills": 0,
                "trueDamageDealt": 0,
                "trueDamageDealtToChampions": 0,
                "trueDamageTaken": 1863,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": true
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 5,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 17000,
                "champLevel": 18,
                "championId": 64,
                "championName": "LeeSin",
                "championTransform": 0,
                "commandPings": 2,
                "consumablesPurchased": 4,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 54752,
                "dangerPings": 0,
                "deaths": 7,
                "detectorWardsPlaced": 0,
                "doubleKills": 0,
                "dragonKills": 0,
                "eligibleForProgression": true,
                "enemyMissingPings": 2,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 19800,
                "goldSpent": 19800,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 226630,
                "item1": 223047,
                "item2": 228001,
                "item3": 223156,
                "item4": 223071,
                "item5": 223075,
                "item6": 3348,
                "itemsPurchased": 12,
                "killingSprees": 1,
                "kills": 6,
                "lane": "NONE",
                "largestCriticalStrike": 0,
                "largestKillingSpree": 4,
                "largestMultiKill": 1,
                "longestTimeSpentLiving": 99,
                "magicDamageDealt": 6328,
                "magicDamageDealtToChampions": 5117,
                "magicDamageTaken": 27457,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 2,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 41907,
                "physicalDamageDealtToChampions": 22943,
                "physicalDamageTaken": 16772,
                "placement": 2,
                "playerAugment1": 68,
                "playerAugment2": 16,
                "playerAugment3": 41,
                "playerAugment4": 82,
                "playerSubteamId": 1,
                "profileIcon": 5916,
                "pushPings": 0,
                "puuid": "Vk1mQcXPtS3twf7WS4k8t3mkp07j2lM1BCRLCDx2Z-8VaVJO_j3r0TTJRjtsrJbXHkRgxaPW3X9teg",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 123,
                "spell2Casts": 44,
                "spell3Casts": 58,
                "spell4Casts": 13,
                "subteamPlacement": 2,
                "summoner1Casts": 1,
                "summoner1Id": 2201,
                "summoner2Casts": 2,
                "summoner2Id": 2202,
                "summonerId": "fJGshhHB0014tvj6i7FOtcF70oPII9FeZtvFOCc-f-egzylm",
                "summonerLevel": 204,
                "summonerName": "Jerboas",
                "teamEarlySurrendered": false,
                "teamId": 100,
                "teamPosition": "",
                "timeCCingOthers": 38,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 48236,
                "totalDamageDealtToChampions": 28060,
                "totalDamageShieldedOnTeammates": 740,
                "totalDamageTaken": 45497,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 7462,
                "totalHealsOnTeammates": 0,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 132,
                "totalTimeSpentDead": 1119,
                "totalUnitsHealed": 1,
                "tripleKills": 0,
                "trueDamageDealt": 0,
                "trueDamageDealtToChampions": 0,
                "trueDamageTaken": 1267,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": true
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 0,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 11000,
                "champLevel": 12,
                "championId": 114,
                "championName": "Fiora",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 0,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 5915,
                "dangerPings": 0,
                "deaths": 6,
                "detectorWardsPlaced": 0,
                "doubleKills": 0,
                "dragonKills": 0,
                "eligibleForProgression": false,
                "enemyMissingPings": 0,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 11350,
                "goldSpent": 2000,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 223184,
                "item1": 223111,
                "item2": 0,
                "item3": 0,
                "item4": 0,
                "item5": 0,
                "item6": 3348,
                "itemsPurchased": 2,
                "killingSprees": 1,
                "kills": 2,
                "lane": "NONE",
                "largestCriticalStrike": 127,
                "largestKillingSpree": 2,
                "largestMultiKill": 1,
                "longestTimeSpentLiving": 92,
                "magicDamageDealt": 132,
                "magicDamageDealtToChampions": 132,
                "magicDamageTaken": 6001,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 3,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 4618,
                "physicalDamageDealtToChampions": 3769,
                "physicalDamageTaken": 2333,
                "placement": 4,
                "playerAugment1": 63,
                "playerAugment2": 59,
                "playerAugment3": 0,
                "playerAugment4": 0,
                "playerSubteamId": 2,
                "profileIcon": 4574,
                "pushPings": 0,
                "puuid": "iBZ9VD8a7x4wZfI5jwLjTeCgS4BU2vfb70SBmkexuh21JVd2Ois5HkIcm41C-SvMQr0plSM0gvf9Rg",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 14,
                "spell2Casts": 3,
                "spell3Casts": 6,
                "spell4Casts": 0,
                "subteamPlacement": 4,
                "summoner1Casts": 0,
                "summoner1Id": 2201,
                "summoner2Casts": 0,
                "summoner2Id": 2202,
                "summonerId": "h26o_A_l6auMaOPsTmwzpXS9CQ7ZBxdPOkhUXjd1IbLH-M1r",
                "summonerLevel": 411,
                "summonerName": "EdwardCullenn",
                "teamEarlySurrendered": false,
                "teamId": 200,
                "teamPosition": "",
                "timeCCingOthers": 1,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 5517,
                "totalDamageDealtToChampions": 4567,
                "totalDamageShieldedOnTeammates": 0,
                "totalDamageTaken": 12683,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 1094,
                "totalHealsOnTeammates": 0,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 14,
                "totalTimeSpentDead": 230,
                "totalUnitsHealed": 1,
                "tripleKills": 0,
                "trueDamageDealt": 765,
                "trueDamageDealtToChampions": 665,
                "trueDamageTaken": 4348,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": false
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 1,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 11000,
                "champLevel": 12,
                "championId": 33,
                "championName": "Rammus",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 0,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 32885,
                "dangerPings": 0,
                "deaths": 6,
                "detectorWardsPlaced": 0,
                "doubleKills": 0,
                "dragonKills": 0,
                "eligibleForProgression": false,
                "enemyMissingPings": 2,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 11350,
                "goldSpent": 11000,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 223047,
                "item1": 223193,
                "item2": 223075,
                "item3": 223001,
                "item4": 222051,
                "item5": 0,
                "item6": 3348,
                "itemsPurchased": 5,
                "killingSprees": 0,
                "kills": 0,
                "lane": "NONE",
                "largestCriticalStrike": 0,
                "largestKillingSpree": 0,
                "largestMultiKill": 0,
                "longestTimeSpentLiving": 100,
                "magicDamageDealt": 7421,
                "magicDamageDealtToChampions": 6208,
                "magicDamageTaken": 10985,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 4,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 2530,
                "physicalDamageDealtToChampions": 1243,
                "physicalDamageTaken": 8156,
                "placement": 4,
                "playerAugment1": 24,
                "playerAugment2": 67,
                "playerAugment3": 0,
                "playerAugment4": 0,
                "playerSubteamId": 2,
                "profileIcon": 5778,
                "pushPings": 0,
                "puuid": "IashVvcF5Aef5xCXO6ThIIX9WmrMFT-cMJ6MO_yD6RnS9RtELWwiOQBJqQRKOPkFWiPwoGjU4Wt4aQ",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 24,
                "spell2Casts": 18,
                "spell3Casts": 15,
                "spell4Casts": 10,
                "subteamPlacement": 4,
                "summoner1Casts": 2,
                "summoner1Id": 2202,
                "summoner2Casts": 9,
                "summoner2Id": 2201,
                "summonerId": "oRCMEIV5gcT-8lD5eb29ZaUQ7gQ3LgApmd6Nd0hSyftrRe33",
                "summonerLevel": 293,
                "summonerName": "Omaxu",
                "teamEarlySurrendered": false,
                "teamId": 200,
                "teamPosition": "",
                "timeCCingOthers": 38,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 9951,
                "totalDamageDealtToChampions": 7452,
                "totalDamageShieldedOnTeammates": 0,
                "totalDamageTaken": 19782,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 4570,
                "totalHealsOnTeammates": 845,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 173,
                "totalTimeSpentDead": 219,
                "totalUnitsHealed": 5,
                "tripleKills": 0,
                "trueDamageDealt": 0,
                "trueDamageDealtToChampions": 0,
                "trueDamageTaken": 641,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": false
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 13,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 17000,
                "champLevel": 18,
                "championId": 61,
                "championName": "Orianna",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 5,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 9313,
                "dangerPings": 0,
                "deaths": 5,
                "detectorWardsPlaced": 0,
                "doubleKills": 0,
                "dragonKills": 0,
                "eligibleForProgression": true,
                "enemyMissingPings": 0,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 20150,
                "goldSpent": 19800,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 226653,
                "item1": 223165,
                "item2": 224628,
                "item3": 223089,
                "item4": 223020,
                "item5": 224629,
                "item6": 3348,
                "itemsPurchased": 15,
                "killingSprees": 1,
                "kills": 2,
                "lane": "NONE",
                "largestCriticalStrike": 0,
                "largestKillingSpree": 2,
                "largestMultiKill": 1,
                "longestTimeSpentLiving": 105,
                "magicDamageDealt": 72702,
                "magicDamageDealtToChampions": 25229,
                "magicDamageTaken": 9035,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 5,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 5302,
                "physicalDamageDealtToChampions": 712,
                "physicalDamageTaken": 7122,
                "placement": 1,
                "playerAugment1": 65,
                "playerAugment2": 84,
                "playerAugment3": 14,
                "playerAugment4": 72,
                "playerSubteamId": 3,
                "profileIcon": 3591,
                "pushPings": 0,
                "puuid": "Dx6wZPz5BOo8wQhtE68kDxAfMf1iXDFIr0KmA7FRBMpfmpT8HzqfBOulL2vaYgL04HMPj_PbdpIx1w",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 116,
                "spell2Casts": 68,
                "spell3Casts": 49,
                "spell4Casts": 8,
                "subteamPlacement": 1,
                "summoner1Casts": 4,
                "summoner1Id": 2202,
                "summoner2Casts": 1,
                "summoner2Id": 2201,
                "summonerId": "eQsaK8yKMbuvrGenhorg67hh5yu-eC7pHjY3-KWjOwzFq6we_Tt9wrtzEg",
                "summonerLevel": 337,
                "summonerName": "Pookie the dog",
                "teamEarlySurrendered": false,
                "teamId": 100,
                "teamPosition": "",
                "timeCCingOthers": 36,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 78004,
                "totalDamageDealtToChampions": 25942,
                "totalDamageShieldedOnTeammates": 4421,
                "totalDamageTaken": 16666,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 268,
                "totalHealsOnTeammates": 0,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 205,
                "totalTimeSpentDead": 724,
                "totalUnitsHealed": 1,
                "tripleKills": 0,
                "trueDamageDealt": 0,
                "trueDamageDealtToChampions": 0,
                "trueDamageTaken": 508,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": true
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 2,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 2,
                "champExperience": 17000,
                "champLevel": 18,
                "championId": 145,
                "championName": "Kaisa",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 1,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 19126,
                "dangerPings": 0,
                "deaths": 2,
                "detectorWardsPlaced": 0,
                "doubleKills": 5,
                "dragonKills": 0,
                "eligibleForProgression": true,
                "enemyMissingPings": 1,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 20150,
                "goldSpent": 22800,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 223036,
                "item1": 223046,
                "item2": 223115,
                "item3": 223124,
                "item4": 226672,
                "item5": 223153,
                "item6": 3348,
                "itemsPurchased": 13,
                "killingSprees": 3,
                "kills": 15,
                "lane": "NONE",
                "largestCriticalStrike": 0,
                "largestKillingSpree": 9,
                "largestMultiKill": 2,
                "longestTimeSpentLiving": 90,
                "magicDamageDealt": 57217,
                "magicDamageDealtToChampions": 23935,
                "magicDamageTaken": 12451,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 6,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 79509,
                "physicalDamageDealtToChampions": 40974,
                "physicalDamageTaken": 9043,
                "placement": 1,
                "playerAugment1": 52,
                "playerAugment2": 72,
                "playerAugment3": 41,
                "playerAugment4": 36,
                "playerSubteamId": 3,
                "profileIcon": 5187,
                "pushPings": 0,
                "puuid": "zM4adBKXIZXy1VX06J8P5hrtBhhPlFGOBHF1fc3I__Mb_c7qn2cVZUy4jfykuRCs7XFrrtuzCGXr6g",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 68,
                "spell2Casts": 53,
                "spell3Casts": 143,
                "spell4Casts": 7,
                "subteamPlacement": 1,
                "summoner1Casts": 2,
                "summoner1Id": 2202,
                "summoner2Casts": 5,
                "summoner2Id": 2201,
                "summonerId": "fmxwkvei5ojJURtTc0WjbBC-v853HexlOmlA99mOzIAgI-I",
                "summonerLevel": 622,
                "summonerName": "Roymand",
                "teamEarlySurrendered": false,
                "teamId": 100,
                "teamPosition": "",
                "timeCCingOthers": 1,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 136726,
                "totalDamageDealtToChampions": 64910,
                "totalDamageShieldedOnTeammates": 0,
                "totalDamageTaken": 21778,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 6378,
                "totalHealsOnTeammates": 0,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 10,
                "totalTimeSpentDead": 1146,
                "totalUnitsHealed": 1,
                "tripleKills": 0,
                "trueDamageDealt": 0,
                "trueDamageDealtToChampions": 0,
                "trueDamageTaken": 283,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": true
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 4,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 12500,
                "champLevel": 13,
                "championId": 876,
                "championName": "Lillia",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 0,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 8359,
                "dangerPings": 0,
                "deaths": 6,
                "detectorWardsPlaced": 0,
                "doubleKills": 0,
                "dragonKills": 0,
                "eligibleForProgression": true,
                "enemyMissingPings": 0,
                "enemyVisionPings": 0,
                "firstBloodAssist": true,
                "firstBloodKill": false,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 13100,
                "goldSpent": 11000,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 223112,
                "item1": 223020,
                "item2": 226653,
                "item3": 224637,
                "item4": 223135,
                "item5": 0,
                "item6": 3348,
                "itemsPurchased": 5,
                "killingSprees": 1,
                "kills": 5,
                "lane": "NONE",
                "largestCriticalStrike": 0,
                "largestKillingSpree": 3,
                "largestMultiKill": 1,
                "longestTimeSpentLiving": 113,
                "magicDamageDealt": 50067,
                "magicDamageDealtToChampions": 23244,
                "magicDamageTaken": 4805,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 7,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 4258,
                "physicalDamageDealtToChampions": 868,
                "physicalDamageTaken": 10742,
                "placement": 3,
                "playerAugment1": 84,
                "playerAugment2": 16,
                "playerAugment3": 14,
                "playerAugment4": 0,
                "playerSubteamId": 4,
                "profileIcon": 5688,
                "pushPings": 0,
                "puuid": "oYMmFzmHEqn-LZnsw0XJEbb-o-_kMiBBJqIny9PGdoi0ZjzmIHtLJ8bOSO5IrbZrN50nn_f6xSBp4g",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 77,
                "spell2Casts": 33,
                "spell3Casts": 45,
                "spell4Casts": 13,
                "subteamPlacement": 3,
                "summoner1Casts": 6,
                "summoner1Id": 2202,
                "summoner2Casts": 14,
                "summoner2Id": 2201,
                "summonerId": "JBx58KZZLzjQqoDZAy0-eLmaz_I28Qt800B9_Gz-n_Rh7Vt8",
                "summonerLevel": 245,
                "summonerName": "Blockerw1z",
                "teamEarlySurrendered": false,
                "teamId": 200,
                "teamPosition": "",
                "timeCCingOthers": 24,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 61767,
                "totalDamageDealtToChampions": 27625,
                "totalDamageShieldedOnTeammates": 0,
                "totalDamageTaken": 15734,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 3367,
                "totalHealsOnTeammates": 0,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 103,
                "totalTimeSpentDead": 165,
                "totalUnitsHealed": 1,
                "tripleKills": 0,
                "trueDamageDealt": 7441,
                "trueDamageDealtToChampions": 3511,
                "trueDamageTaken": 186,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": false
            },
            {
                "allInPings": 0,
                "assistMePings": 0,
                "assists": 5,
                "baitPings": 0,
                "baronKills": 0,
                "basicPings": 0,
                "bountyLevel": 0,
                "champExperience": 12500,
                "champLevel": 13,
                "championId": 42,
                "championName": "Corki",
                "championTransform": 0,
                "commandPings": 0,
                "consumablesPurchased": 0,
                "damageDealtToBuildings": 0,
                "damageDealtToObjectives": 0,
                "damageDealtToTurrets": 0,
                "damageSelfMitigated": 9710,
                "dangerPings": 0,
                "deaths": 5,
                "detectorWardsPlaced": 0,
                "doubleKills": 0,
                "dragonKills": 0,
                "eligibleForProgression": true,
                "enemyMissingPings": 0,
                "enemyVisionPings": 0,
                "firstBloodAssist": false,
                "firstBloodKill": true,
                "firstTowerAssist": false,
                "firstTowerKill": false,
                "gameEndedInEarlySurrender": false,
                "gameEndedInSurrender": false,
                "getBackPings": 0,
                "goldEarned": 13100,
                "goldSpent": 11000,
                "holdPings": 0,
                "individualPosition": "Invalid",
                "inhibitorKills": 0,
                "inhibitorTakedowns": 0,
                "inhibitorsLost": 0,
                "item0": 0,
                "item1": 226671,
                "item2": 226673,
                "item3": 226676,
                "item4": 223006,
                "item5": 223184,
                "item6": 3348,
                "itemsPurchased": 5,
                "killingSprees": 0,
                "kills": 4,
                "lane": "NONE",
                "largestCriticalStrike": 330,
                "largestKillingSpree": 0,
                "largestMultiKill": 1,
                "longestTimeSpentLiving": 106,
                "magicDamageDealt": 29567,
                "magicDamageDealtToChampions": 14339,
                "magicDamageTaken": 5658,
                "needVisionPings": 0,
                "neutralMinionsKilled": 0,
                "nexusKills": 0,
                "nexusLost": 0,
                "nexusTakedowns": 0,
                "objectivesStolen": 0,
                "objectivesStolenAssists": 0,
                "onMyWayPings": 0,
                "participantId": 8,
                "pentaKills": 0,
                "perks": {
                    "statPerks": {
                        "defense": 0,
                        "flex": 0,
                        "offense": 0
                    },
                    "styles": [
                        {
                            "description": "primaryStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        },
                        {
                            "description": "subStyle",
                            "selections": [
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                },
                                {
                                    "perk": 0,
                                    "var1": 0,
                                    "var2": 0,
                                    "var3": 0
                                }
                            ],
                            "style": 0
                        }
                    ]
                },
                "physicalDamageDealt": 7199,
                "physicalDamageDealtToChampions": 2884,
                "physicalDamageTaken": 10673,
                "placement": 3,
                "playerAugment1": 84,
                "playerAugment2": 47,
                "playerAugment3": 1,
                "playerAugment4": 0,
                "playerSubteamId": 4,
                "profileIcon": 5414,
                "pushPings": 0,
                "puuid": "MsNtGO8V4cCqzJKHnI5CvKXp2tX1avVl1LtrWdI7I_Od72iCVvt_gAp6drjc7AHFX2kSgTx1aEJN6Q",
                "quadraKills": 0,
                "riotIdName": "",
                "riotIdTagline": "",
                "role": "SUPPORT",
                "sightWardsBoughtInGame": 0,
                "spell1Casts": 23,
                "spell2Casts": 19,
                "spell3Casts": 13,
                "spell4Casts": 44,
                "subteamPlacement": 3,
                "summoner1Casts": 7,
                "summoner1Id": 2201,
                "summoner2Casts": 4,
                "summoner2Id": 2202,
                "summonerId": "OTC0IqKMr_U_I28ikgjcp73sHxE2KTbrc1XVawSRUKfRfwo",
                "summonerLevel": 241,
                "summonerName": "Imma Be A Star",
                "teamEarlySurrendered": false,
                "teamId": 200,
                "teamPosition": "",
                "timeCCingOthers": 6,
                "timePlayed": 961,
                "totalAllyJungleMinionsKilled": 0,
                "totalDamageDealt": 58637,
                "totalDamageDealtToChampions": 17493,
                "totalDamageShieldedOnTeammates": 0,
                "totalDamageTaken": 16376,
                "totalEnemyJungleMinionsKilled": 0,
                "totalHeal": 3460,
                "totalHealsOnTeammates": 0,
                "totalMinionsKilled": 0,
                "totalTimeCCDealt": 436,
                "totalTimeSpentDead": 413,
                "totalUnitsHealed": 1,
                "tripleKills": 0,
                "trueDamageDealt": 21869,
                "trueDamageDealtToChampions": 269,
                "trueDamageTaken": 43,
                "turretKills": 0,
                "turretTakedowns": 0,
                "turretsLost": 0,
                "unrealKills": 0,
                "visionClearedPings": 0,
                "visionScore": 0,
                "visionWardsBoughtInGame": 0,
                "wardsKilled": 0,
                "wardsPlaced": 0,
                "win": false
            }
        ],
        "platformId": "NA1",
        "queueId": 1700,
        "teams": [
            {
                "bans": [
                    {
                        "championId": 74,
                        "pickTurn": 1
                    },
                    {
                        "championId": 17,
                        "pickTurn": 2
                    },
                    {
                        "championId": 10,
                        "pickTurn": 3
                    },
                    {
                        "championId": 44,
                        "pickTurn": 4
                    },
                    {
                        "championId": 27,
                        "pickTurn": 5
                    },
                    {
                        "championId": 106,
                        "pickTurn": 6
                    },
                    {
                        "championId": 1,
                        "pickTurn": 7
                    },
                    {
                        "championId": 19,
                        "pickTurn": 8
                    }
                ],
                "objectives": {
                    "baron": {
                        "first": false,
                        "kills": 0
                    },
                    "champion": {
                        "first": false,
                        "kills": 16
                    },
                    "dragon": {
                        "first": false,
                        "kills": 0
                    },
                    "inhibitor": {
                        "first": false,
                        "kills": 0
                    },
                    "riftHerald": {
                        "first": false,
                        "kills": 0
                    },
                    "tower": {
                        "first": false,
                        "kills": 0
                    }
                },
                "teamId": 100,
                "win": true
            },
            {
                "bans": [],
                "objectives": {
                    "baron": {
                        "first": false,
                        "kills": 0
                    },
                    "champion": {
                        "first": false,
                        "kills": 0
                    },
                    "dragon": {
                        "first": false,
                        "kills": 0
                    },
                    "inhibitor": {
                        "first": false,
                        "kills": 0
                    },
                    "riftHerald": {
                        "first": false,
                        "kills": 0
                    },
                    "tower": {
                        "first": false,
                        "kills": 0
                    }
                },
                "teamId": 0,
                "win": false
            }
        ],
        "tournamentCode": ""
    }
}"""
handler.addMatch(str)
