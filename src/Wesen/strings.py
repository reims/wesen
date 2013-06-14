"""string definitions"""

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
	"ENABLEGUI (deprecated)":"\nenablegui=",
	"GUISOURCE (deprecated)":"(destination of your gui sourcecode, leave blank if disabled)\nguisource=",
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
	python %prog [options]
	./wesen.py action [options]

	action:		d for the daemon, c for the configed, h to print this string, p for profiling
			cd for config defaults creation, cp for profiling config creation
			dd for config defaults daemon running
	options:	are directly passed to the started string
		""";

STRING_USAGE_WESEND = """usage:
	python %prog [options]
	./%prog [options]
		""";
STRING_USAGE_WESEND_DISABLEGUI = "don't use a GUI";
STRING_USAGE_WESEND_ENABLEGUI = "use a GUI";
STRING_USAGE_WESEND_GUISOURCE = "specify GUI source destination";
STRING_USAGE_WESEND_QUIET = "stop logging";
STRING_USAGE_WESEND_LOGFILE = "specify logfile";
STRING_USAGE_WESEND_CONFIGFILE = "specify configfile";

STRING_LOGGER = {
"DEATHWESEN":{
	"AGE":"%s died because of too high age",
	"ATTACK":"%s was attacked with %s energy",
	"ENERGY":"%s died because of too low energy level"},
"DEATHFOOD":{
	"AGE":"food %s was removed because of too high age",
	"ENERGY":"food %s was removed because of too high energy level"}};
