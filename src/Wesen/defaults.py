"""config defaults"""

from .definition import DIMENSIONS;
from os.path import expanduser, join;

DEFAULT_GENERAL_CONFIGFILE = join(expanduser("~"),".wesen","conf"); # this configfile is _always_ used before any other specified!
DEFAULT_GENERAL_CONFIGFILE_PROFILE = join(expanduser("~"),".wesen","conf_profile"); # used for profiling devtools
# these default values are used in configed for the defaults in the editor and when no values are specified in the configfile.
# I recommend to use the calculated values as they are.
DEFAULT_GUI_ENABLE = 1;
DEFAULT_GUI_SOURCE = "gui";
DEFAULT_GUI_SIZE = 800;
DEFAULT_GUI_POS = "50,50";
DEFAULT_GUI_MAP = True;
DEFAULT_GUI_GRAPH = True;
DEFAULT_GUI_TEXT = True;

DEFAULT_GENERAL_ENABLEGUI = 1; # deprecated
DEFAULT_GENERAL_GUISOURCE = "gui"; # deprecated
DEFAULT_GENERAL_ENABLELOG = True;
DEFAULT_GENERAL_LOGFILE = join(expanduser("~"),".wesen","log");

DEFAULT_WORLD_LENGTH = 1000;

DEFAULT_WESEN_SOURCES = "DrunkenSailor,Scanner,Nightwatch";
DEFAULT_WESEN_COUNT = 20;
DEFAULT_WESEN_ENERGY = 100;
DEFAULT_WESEN_MAXAGE = 500;

DEFAULT_FOOD_COUNT = 10*DEFAULT_WESEN_COUNT;
DEFAULT_FOOD_AMOUNT = 1;
DEFAULT_FOOD_MAXAMOUNT = DEFAULT_WESEN_ENERGY * 10000;
DEFAULT_FOOD_MAXAGE = DEFAULT_WESEN_MAXAGE * 10000;
DEFAULT_FOOD_SEEDRATE = 1;
DEFAULT_FOOD_GROWRATE = 2;

DEFAULT_TIME_LOOK = 1;
DEFAULT_TIME_CLOSERLOOK = 2;
DEFAULT_TIME_MOVE = 4;
DEFAULT_TIME_EAT = 3;
DEFAULT_TIME_TALK = 1;
DEFAULT_TIME_VOMIT = 5;
DEFAULT_TIME_BROADCAST = int(DEFAULT_TIME_TALK * 1.2);
DEFAULT_TIME_ATTACK = 7;
DEFAULT_TIME_DONATE = DEFAULT_TIME_TALK + DEFAULT_TIME_VOMIT;
DEFAULT_TIME_REPRODUCE = 16;
DEFAULT_TIME_INIT = DEFAULT_TIME_REPRODUCE * 2 - 1;
DEFAULT_TIME_MAX = DEFAULT_TIME_INIT * 2;

DEFAULT_RANGE_SEED = 12;
DEFAULT_RANGE_LOOK = 3;
DEFAULT_RANGE_TALK = 14;
