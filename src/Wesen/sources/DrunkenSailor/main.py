"""
the drunken sailor is a simple implementation of random movement.
"""

from ...defaultwesensource import DefaultWesenSource
from random import choice


class WesenSource(DefaultWesenSource):

    def __init__(self, infoAllSource):
        """Do all initialization stuff."""
        DefaultWesenSource.__init__(self, infoAllSource)
        self.randRange = [-1, 0, 1]

    def __str__(self):
        return "<Sailor, hasn't been on any boat yet>"

    def main(self):
        while(self.time() > self.infoTime["move"]):
            self.Move([choice(self.randRange), choice(self.randRange)])
            edible = [o for o in self.closerLook() if o["type"] == "food" and o[
                "position"] == self.position]
            if(edible):
                self.Eat(edible[0]["id"])
