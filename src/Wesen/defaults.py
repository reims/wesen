"""config defaults"""

from os.path import expanduser, join;
from math import sqrt;

DEFAULT_GENERAL_CONFIGFILE = join(expanduser("~"),".wesen","conf");
# this configfile is _always_ used before any other specified!
# these default values are used in configed for the defaults in the editor and when no values are specified in the configfile.
# I recommend to use the calculated values as they are.
# For an explanation of these values,
# run the config editor (with wesen --editconfig)

DEFAULT_GENERAL_ENABLELOG = False;
DEFAULT_GENERAL_LOGFILE = join(expanduser("~"),".wesen","log");

DEFAULT_WORLD_LENGTH = 500;

DEFAULT_WESEN_SOURCES = "Rincewind,Nightwatch,Dwarf";
DEFAULT_WESEN_COUNT = 5;
DEFAULT_WESEN_ENERGY = 300;
DEFAULT_WESEN_MAXAGE = 1000;

DEFAULT_FOOD_COUNT = int(sqrt(DEFAULT_WORLD_LENGTH))*DEFAULT_WESEN_COUNT*5;
DEFAULT_FOOD_ENERGY = 10;
DEFAULT_FOOD_MAXAMOUNT = DEFAULT_WESEN_ENERGY * 10;
DEFAULT_FOOD_MAXAGE = DEFAULT_WESEN_MAXAGE;
DEFAULT_FOOD_SEEDRATE = 0.001; # in percent
DEFAULT_FOOD_GROWRATE = 0.3;  # in percent

DEFAULT_RANGE_SEED = 10;
DEFAULT_RANGE_LOOK = 25;
DEFAULT_RANGE_CLOSER_LOOK = 15;
DEFAULT_RANGE_TALK = 15;

DEFAULT_TIME_LOOK = 1;
DEFAULT_TIME_CLOSERLOOK = 2;
DEFAULT_TIME_MOVE = 7;
DEFAULT_TIME_EAT = 10;
DEFAULT_TIME_TALK = 1;
DEFAULT_TIME_VOMIT = 12;
DEFAULT_TIME_BROADCAST = int(DEFAULT_TIME_TALK * 1.2);
DEFAULT_TIME_ATTACK = 14;
DEFAULT_TIME_DONATE = DEFAULT_TIME_TALK + DEFAULT_TIME_VOMIT;
DEFAULT_TIME_REPRODUCE = 20;
DEFAULT_TIME_INIT = int(DEFAULT_TIME_REPRODUCE * 1.2);
DEFAULT_TIME_MAX = DEFAULT_TIME_INIT * 2;

DEFAULT_GUI_ENABLE = 1;
DEFAULT_GUI_SOURCE = "gui";
DEFAULT_GUI_SIZE = 500;
DEFAULT_GUI_POS = "50,50";
DEFAULT_GUI_MAP = True;
DEFAULT_GUI_GRAPH = True;
DEFAULT_GUI_TEXT = True;
