"""
    Contains functions to verify if a region is valid, or to attempt to fix it if it is not.
    Region objects should be used in all instances, other than when you are initializing one after a command is triggered.
"""


class Region:
    def __init__(self, temp_region):
        """Attempts to correct the given region, and then verifies that it is valid."""
        self.region = temp_region
        self.region = self.correct_region()  # Initialize self.region
        self.route = self.reroute_region()  # Find the route value
        self.is_valid = self.verify_region()  # Verify if it is a valid region


    def verify_region(self):
        """Returns true if the given region is valid. Otherwise, returns false. Call this after correctRegion()."""
        regions = {'br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru', 'ph2', 'sg2', 'th2',
                   'tw2', 'vn2'}
        region = self.region.lower()
        if region in regions:
            return True
        return False


    def correct_region(self):
        """Attempt to correct a given region to work with API. i.e. 'na' -> 'na1'"""
        temp_region = self.region.lower()
        if temp_region == 'na':
            return 'na1'
        if temp_region == 'br':
            return 'br1'
        if temp_region == 'lan':
            return 'la1'
        if temp_region == 'las':
            return 'la2'
        if temp_region == 'eune':
            return 'eun1'
        if temp_region == 'euw':
            return 'euw1'
        if temp_region == "tr":
            return 'tr1'
        if temp_region == 'jp':
            return 'jp1'
        if temp_region == 'oce':
            return 'oc1'
        return temp_region


    def reroute_region(self):
        """Reroute a given region. Ex: 'na1' -> 'americas'"""
        americas = {'na1', 'br1', 'la1', 'la2'}
        europe = {'euw1', 'eun1', 'tr1', 'ru'}
        asia = {'jp1', 'kr'}
        sea = {'oc1', 'ph2', 'sg2', 'th2', 'tw2', 'vn2'}
        if self.region in americas:
            return 'americas'
        if self.region in europe:
            return 'europe'
        if self.region in asia:
            return 'asia'
        if self.region in sea:
            return 'sea'
        return self.region  # Return the region if it can't be found
