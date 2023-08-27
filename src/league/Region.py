"""
    Contains functions to verify if a region is valid, or to attempt to fix it if it is not.
    Region objects should be used in all instances, other than when you are initializing one after a command is triggered.
"""


class Region:
    def __init__(self, tempRegion):
        """Attempts to correct the given region, and then verifies that it is valid."""
        self.region = tempRegion  # Initialize self.region
        self.region = self.correctRegion()  # Correct self.region
        self.route = self.rerouteRegion()  # Find the route value
        self.isValid = self.verifyRegion()  # Verify if it is a valid region


    def verifyRegion(self):
        """Returns true if the given region is valid. Otherwise, returns false. Call this after correctRegion()."""
        regions = {'br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru', 'ph2', 'sg2', 'th2',
                   'tw2', 'vn2'}
        region = self.region.lower()
        if region in regions:
            return True
        return False


    def correctRegion(self):
        """Attempt to correct a given region to work with API. i.e. 'na' -> 'na1'"""
        tempRegion = self.region.lower()
        if tempRegion == 'na':
            return 'na1'
        if tempRegion == 'br':
            return 'br1'
        if tempRegion == 'lan':
            return 'la1'
        if tempRegion == 'las':
            return 'la2'
        if tempRegion == 'eune':
            return 'eun1'
        if tempRegion == 'euw':
            return 'euw1'
        if tempRegion == "tr":
            return 'tr1'
        if tempRegion == 'jp':
            return 'jp1'
        if tempRegion == 'oce':
            return 'oc1'
        return tempRegion


    def rerouteRegion(self):
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
