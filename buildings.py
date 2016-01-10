from importer import * # noqa


class BuildingManager(object):
    def __init__(self, library):
        self.library = library

    def lookup(self, key):
        return self.library[key]
