"""Unit tests for persistence via JSON"""

if __name__ == "__main__":
    import sys;
    sys.path.append("../src");

import unittest
from Wesen.world import World;
from Wesen.defaults import DEFAULT_CONFIGFILE;
from Wesen.configed import ConfigEd;
from Wesen.wesend import Wesend;

class TestPersistence(unittest.TestCase):
    
    def setUp(self):
        configEd = ConfigEd(DEFAULT_CONFIGFILE);
        config = configEd.getConfig();
        wesend = Wesend(config);
        self.world = wesend.world;

    def test_consistency(self):
        """Basic consistency check.
        Checks that a world created from the persistence info of another 
        world returns the same persistence info"""
        d = self.world.persist();
        world2 = World(d, createObjects=False);
        world2.restore(d);
        d2 = world2.persist();
        #have to sort objects, since their order is arbitrary
        d2["objects"].sort(key = lambda o: (o["type"],  o["energy"], o["source"], tuple(o["position"])));
        d["objects"].sort(key = lambda o: (o["type"],  o["energy"], o["source"], tuple(o["position"])));
        self.assertTrue(d == d2, "Restored world returned different persistency info than original world");

    def test_conistency_with_json(self):
        string = self.world.persistToJSON();
        world2 = World();
        world2.restoreFromJson(string);
        d = self.world.persist();
        d2 = world2.persist();
        #have to sort objects, since their order is arbitrary
        d2["objects"].sort(key = lambda o: (o["type"],  o["energy"], o["source"], tuple(o["position"])));
        d["objects"].sort(key = lambda o: (o["type"],  o["energy"], o["source"], tuple(o["position"])));
        self.assertTrue(d == d2, "Restored world returned different persistency info than original world");

if __name__ == "__main__":
    unittest.main();
