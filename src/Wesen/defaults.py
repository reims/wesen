"""config defaults

For an explanation of these values,
run the config editor (with wesen --editconfig)"""

from os.path import expanduser, join;
from math import sqrt;

#HINT: While the following could be inferred from the defaults below,
#      It adds a lot of clarity to have it explicitly.
CONFIG_OPTIONS = [["general",
                   [("enablelog", bool),
                    ("logfile", str)]],
		  ["gui",
                   [("enable", bool),
                    ("source", str),
                    ("size", int),
                    ("pos", str)]],        # x,y
		  ["world",
                   [("length", int)]],
		  ["wesen",
                   [("sources", str),      # comma-separated
                    ("count", int),
                    ("energy", int),
                    ("maxage", int)]],
		  ["food",
                   [("count", int),
                    ("energy", int),
                    ("maxamount", int),
                    ("maxage", int),
                    ("growrate", float),   # in percent
                    ("seedrate", float)]], # in percent
		  ["range",
                   [("look", int),
                    ("closer_look", int),
                    ("talk", int),
                    ("seed", int)]],
		  ["time",
                   [("init", int),
                    ("max", int),
                    ("look", int),
                    ("closerlook", int),
                    ("move", int),
                    ("eat", int),
                    ("talk", int),
                    ("vomit", int),
                    ("broadcast", int),
                    ("attack", int),
                    ("donate", int),
                    ("reproduce", int)]]];

CONFIG_DEFAULTS = {"general":
                       {"enablelog":False,
                        "logfile":join(expanduser("~"),".wesen","log")},
                   "gui":
                       {"enable":True,
                        "source":"gui",
                        "size":500,
                        "pos":"50,50"},
                   "world":
                       {"length":500},
                   "wesen":
                       {"sources":"Rincewind,Nightwatch,Dwarf",
                        "count":5,
                        "energy":300,
                        "maxage":1000},
                   "food":
                       {"count":600,
                        "energy":10,
                        "maxamount":1000,
                        "seedrate":0.002,
                        "growrate":0.2,
                        "maxage":1000},
                   "range":
                       {"seed":10,
                        "look":24,
                        "closer_look":12,
                        "talk":16},
                   "time":
                       {"init":25,
                        "max":50,
                        "look":1,
                        "closerlook":2,
                        "talk":1,
                        "broadcast":1,
                        "move":7,
                        "eat":10,
                        "vomit":12,
                        "donate":13,
                        "attack":14,
                        "reproduce":20}
                   };

DEFAULT_CONFIGFILE = join(expanduser("~"),".wesen","conf");
