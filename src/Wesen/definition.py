"""fix values"""

from os.path import expanduser, join;

NAMES = dict(PROJECT="wesen", WESEND="wesend", CONFIGED="configed", GUI = "gui");
VERSIONS = dict(PROJECT="0.6.dev", WESEND="0.6", CONFIGED="0.6", GUI = "0.6");

# change these values only here, they are not included in any configfiles!
DIMENSIONS = 2; # must be 2 at this time. perhaps it will be 3 by default some day.
FORMAT_LOGSTRING = "%(asctime)s %(levelname)s %(message)s";

PROFILE_WESEND = join(expanduser("~"),".wesen","profiletemp~");
