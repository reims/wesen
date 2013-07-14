"""string definitions"""

from .defaults import DEFAULT_GENERAL_CONFIGFILE, DEFAULT_GAME_STATE_FILE;

# for I18N, insert here a stringtable-loader or replace this file.

STRING_ERROR_NOTSAMEPATH = "There is a path problem. The program could not find the desired files.";
STRING_ERROR_FILEEXISTS = "file %s already exists, overwrite? (y, n) ";
STRING_ERROR_NOTWROTE = "didn't write file %s";


STRING_MESSAGE_WROTE = "wrote file %s";
STRING_MESSAGE_PROCESSING = "processing file %s";
STRING_MESSAGE_REMOVED = "removed file %s";


STRING_CONFIGED = {
"WESEN":{
	"SOURCES":"(comma-seperated wesen sources)\nsources=",
	"COUNT":"(how much wesen are created during startup from each source)\ncount=",
	"ENERGY":"(starting energy of every wesen at the beginning)\nenergy=",
	"MAXAGE":"(maximum age of wesen until they die)\nmaxage="},
"GUI":{
	"ENABLE":"\nenable=",
	"SOURCE":"\nsource=",
	"SIZE":"\nsize=",
	"POS":"\npos=",
	"MAP":"\nmap=",
	"GRAPH":"\ngraph=",
	"TEXT":"\ntext="},
"WORLD":{
	"LENGTH":"(length of the worlds x-axis and y-axis)\nlength="},
"FOOD":{
	"COUNT":"(how many food places at start)\ncount=",
	"ENERGY":"(starting energy of every food place at the beginning)\namount=",
	"MAXAMOUNT":"(maximum food amount without growth stop)\nmaxamount=",
	"MAXAGE":"(maximum age without self-destruction)\nmaxage=",
	"SEEDRATE":"(in %, 100 means every, 1 means every 100th round)\nseedrate=",
	"GROWRATE":"(in %, 100 means every, 1 means every 100th round)\ngrowrate="},
"RANGE":{
	"LOOK":"(how far the wesen can look)\nlook=",
	"CLOSER_LOOK":"(how far the wesen can look closely)\nlook=",
	"TALK":"(how \"far\" the wesen can talk)\ntalk=",
	"SEED":"(how far the food can seed)\nseed="},
"TIME":{
	"INIT":"(time a wesen gets each turn)\ninit=",
	"MAX":"(maximum time a wesen can have in a turn)\nmax=",
	"LOOK":"(time needed for looking around)\nlook=",
	"CLOSERLOOK":"(time needed for a closer look)\ncloserlook=",
	"MOVE":"(time needed for moving)\nmove=",
	"EAT":"(time needed for eating)\neat=",
	"TALK":"(time needed for talking)\ntalk=",
	"VOMIT":"(time needed for vomiting)\nvomit=",
	"ATTACK":"(time needed for attacking)\nattack=",
	"BROADCAST":"(time needed for broadcasting)\nbroadcast=",
	"DONATE":"(time needed for donations)\ndonate=",
	"REPRODUCE":"(time needed for reproduction)\nreproduce="}};

STRING_USAGE_DESCRIPTION = 'Predator-prey simulation for learning python and AI. See also https://github.com/reims/wesen';
STRING_USAGE_CONFIGFILE = 'specify the configfile to use, defaults to '+DEFAULT_GENERAL_CONFIGFILE;
STRING_USAGE_EDITCONFIG = 'start the config editor';
STRING_USAGE_DEFAULTCONFIG = 'write the default config';
STRING_USAGE_PRINTCONFIG = 'print the config (without changes from command-line options)';
STRING_USAGE_OVERWRITE = 'overwrite config [%s] %s';
STRING_USAGE_RESUME = 'resumes game stored in %s if exists' % DEFAULT_GAME_STATE_FILE;
STRING_USAGE_EPILOG = 'all other arguments are passed to OpenGL';

