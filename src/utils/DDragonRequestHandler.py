import requests


class DDragonRequestHandler:
    def __init__(self):
        pass


    @staticmethod
    def getLatestVersion():
        """Returns the latest version of League of Legends."""
        url = 'https://ddragon.leagueoflegends.com/api/versions.json'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error: {response.status_code}, {response.reason}')
            return None
        return response.json()[0]


    def getProfileIconURL(self, profileIconId):
        """Returns the URL to obtain a profile picture given a profileIconId"""
        version = self.getLatestVersion()
        if version is None:  # If version can't be found, use a default
            version = '13.15.1'
        url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profileIconId}.png'
        return url


    def getChampSplashURL(self, champStr):
        """Returns the URL to obtain a champion splash art given its name. i.e. 'Aatrox_0'."""
        url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champStr}.jpg'
        return url


    def getChampLoadingURL(self, champStr):
        """Returns the URL to obtain a champion loading screen given its name. i.e. 'Aatrox_0'."""
        url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champStr}.jpg'
        return url
