"""string definitions"""

from .defaults import DEFAULT_GENERAL_CONFIGFILE;

# for I18N, insert here a stringtable-loader or replace this file.

STRING_ERROR_NOTSAMEPATH = "There is a path problem. The program could not find the desired files.";
STRING_ERROR_FILEEXISTS = "file %s already exists, overwrite? (y, n) ";
STRING_ERROR_NOTWROTE = "didn't write %s";


STRING_MESSAGE_WROTE = "	wrote %s";
STRING_MESSAGE_PROCESSING = "	processing %s";
STRING_MESSAGE_REMOVED = "	removed %s";


STRING_CONFIGED = {
"WESEN":{
	"SOURCES":"(comma-seperated wesen sources)\nsources=",
	"COUNT":"(how much wesen are created during startup from each source)\ncount=",
	"ENERGY":"(starting energy of every wesen)\nenergy=",
	"MAXAGE":"(maximum age of wesen until they die)\nmaxage="},
"GUI":{
	"ENABLE":"\nenable=",
	"SOURCE":"\nsource=",
	"SIZE":"\nsize=",
	"POS":"\npos=",
	"MAP":"\nmap=",
	"GRAPH":"\ngraph=",
	"TEXT":"\ntext="},
"GENERAL":{
	"ENABLELOG":"\nenablelog=",
	"LOGFILE":"(destination of your logfile, leave blank if disabled)\nlogfile="},
"WORLD":{
	"LENGTH":"(length of the worlds x-axis and y-axis and perhaps other, too)\nlength="},
"FOOD":{
	"COUNT":"(how many food places at start)\ncount=",
	"AMOUNT":"(starting energy of every food place)\namount=",
	"MAXAMOUNT":"(maximum food amount without self-destruction)\nmaxamount=",
	"MAXAGE":"(maximum age without self-destruction)\nmaxage=",
	"SEEDRATE":"(in %, 100 means every, 1 means every 100th round)\nseedrate=",
	"GROWRATE":"(in %, 100 means every, 1 means every 100th round)\ngrowrate="},
"RANGE":{
	"LOOK":"(how far the wesen can look)\nlook=",
	"CLOSER_LOOK":"(how far the wesen can look closely)\nlook=",
	"TALK":"(how \"far\" the wesen can talk)\ntalk=",
	"SEED":"(how far the food can seed)\nseed="},
"TIME":{
	"INIT":"(time a wesen gets when it's \"born\")\ninit=",
	"MAX":"(maximum time a wesen can have)\nmax=",
	"LOOK":"(time needed for looking)\nlook=",
	"CLOSERLOOK":"(time needed for a closer look)\ncloserlook=",
	"MOVE":"(time needed for moving)\nmove=",
	"EAT":"(time needed for eating)\neat=",
	"TALK":"(time needed for moving)\ntalk=",
	"VOMIT":"(time needed for vomiting)\nvomit=",
	"ATTACK":"(time needed for attacking)\nattack=",
	"BROADCAST":"(time needed for moving)\nbroadcast=",
	"DONATE":"(time needed for moving)\ndonate=",
	"REPRODUCE":"(time needed for reproduce)\nreproduce="}};


STRING_USAGE_LOADER = """usage:
	python3 wesen [options]
	
		print this help message
			--help
		specify config file to use:
			--configfile=~/.wesen/conf
		to start the config editor to write to a configfile:
			--editconfig
		to write the default config to a configfile (ignored if --editconfig):
			--defaultconfig
		to overwrite certain options from the config file:
			--enablegui, --disablegui
			--enablelogger, --disablelogger
			--logfile=~/.wesen/log
			--sources=Nightwatch,Dwarf

		all other arguments are passed to OpenGL
		
		to get more help, look at
			https://github.com/reims/wesen
		""";
STRING_USAGE_DESCRIPTION = 'Predator-prey simulation for learning python and AI. See also https://github.com/reims/wesen';
STRING_USAGE_CONFIGFILE = 'specify the configfile to use, defaults to '+DEFAULT_GENERAL_CONFIGFILE;
STRING_USAGE_EDITCONFIG = 'start the config editor';
STRING_USAGE_DEFAULTCONFIG = 'write the default config';
STRING_USAGE_PRINTCONFIG = 'print the config (without changes from command-line options)';
STRING_USAGE_OVERWRITE = 'overwrite corresponding setting in the config file';
STRING_USAGE_EPILOG = 'all other arguments are passed to OpenGL';

STRING_LOGGER = {
"DEATHWESEN":{
	"AGE":"%s died because of too high age",
	"ATTACK":"%s was attacked with %s energy",
	"ENERGY":"%s died because of too low energy level"},
"DEATHFOOD":{
	"AGE":"food %s was removed because of too high age",
	"ENERGY":"food %s was removed because of too high energy level"}};
