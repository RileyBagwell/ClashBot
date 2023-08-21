from ClashBot.src.utils.RiotRequestHandler import RiotRequestHandler


class RiotRequestHandlerTest:
    def __init__(self):
        self.handler = RiotRequestHandler()  # Create request handler
        #self.getSummonerByNameTest()  # Test getSummonerByName
        #self.getPuuidByNameTest()  # Test getPuuidByName
        #self.getMatchesByPuuidTest()  # Test getMatchesByPuuid
        self.getMatchByMatchIdTest()  # Test getMatchByMatchId


    def getSummonerByNameTest(self):
        summoner = self.handler.getSummonerByName('NA1', 'Blockerw1z')
        if summoner is None:
            print('Summoner was not found.')
            return
        print(f'accountId: {summoner.accountId}\nprofileIconId: {summoner.profileIconId}')
        print(f'revisionDate: {summoner.revisionDate}\nname: {summoner.name}')
        print(f'id: {summoner.id}\npuuid: {summoner.puuid}\nsummonerLevel: {summoner.summonerLevel}\n')


    def getPuuidByNameTest(self):
        print(f'puuid: {self.handler.getPuuidByName("NA1", "Blockerw1z")}\n')


    def getMatchesByPuuidTest(self):
        tempPuuid = 'oYMmFzmHEqn-LZnsw0XJEbb-o-_kMiBBJqIny9PGdoi0ZjzmIHtLJ8bOSO5IrbZrN50nn_f6xSBp4g'
        print(f'Matches: {self.handler.getMatchesByPuuid("americas", tempPuuid, 5)}\n')


    def getMatchByMatchIdTest(self):
        match = self.handler.getMatchByMatchId('americas', 'NA1_4732822116')
        #print(f'dataVersion: {match.dataVersion}\nmatchId: {match.matchId}\nparticipants: {match.participants}')
        #print(f'gameMode: {match.gameMode}\nteams: {match.teams}')
        #print(match.teams[0].teamId)
        #print(match.teams[0].bans[0].championId)
        print(match.participants[0].assists)


testHandler = RiotRequestHandlerTest()  # Test handler object
