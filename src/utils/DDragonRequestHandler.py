import requests


class DDragonRequestHandler:
    def __init__(self):
        pass


    @staticmethod
    def get_latest_version():
        """Returns the latest version of League of Legends."""
        url = 'https://ddragon.leagueoflegends.com/api/versions.json'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error: {response.status_code}, {response.reason}')
            return None
        return response.json()[0]


    def get_profile_icon_url(self, profile_icon_id):
        """Returns the URL to obtain a profile picture given a profileIconId"""
        version = self.get_latest_version()
        if version is None:  # If version can't be found, use a default
            version = '13.15.1'
        url = f'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profile_icon_id}.png'
        return url


    def get_champ_splash_url(self, champ_str):
        """Returns the URL to obtain a champion splash art given its name. i.e. 'Aatrox_0'."""
        url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ_str}.jpg'
        return url


    def get_champ_loading_url(self, champ_str):
        """Returns the URL to obtain a champion loading screen given its name. i.e. 'Aatrox_0'."""
        url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_str}.jpg'
        return url
