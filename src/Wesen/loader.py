"""The Loader function determines which configfile to use
and interprets command-line arguments.
It then runs a Wesend instance."""

from .definition import NAMES, VERSIONS;
from .defaults import DEFAULT_GENERAL_CONFIGFILE;
from .strings import STRING_USAGE_PRINTCONFIG, \
		     STRING_USAGE_DEFAULTCONFIG, \
		     STRING_USAGE_EDITCONFIG, \
		     STRING_USAGE_CONFIGFILE, \
		     STRING_USAGE_EPILOG, \
		     STRING_USAGE_DESCRIPTION, \
		     STRING_USAGE_RESUME, \
		     STRING_USAGE_OVERWRITE;
from .configed import ConfigEd;
from .wesend import Wesend;
from argparse import ArgumentParser, Action;
from os import mkdir;
from os.path import exists, join, expanduser;
import importlib;
import sys;

def Loader(run_immediately=True):
	"""Calling a Loader object will start a Wesen simulation,
	if the found configuration allows it.

	First, looks for the config file location
	provided by command-line (or using a fallback).
	Then, using ConfigEd, getting the config
	(using fallback config from defaults.py)
	and modifying it according to command-line parameters.
	Then it checks whether the provided sources exist,
	and runs a Wesen simulation with the given config.

	If you want to manipulate the Wesen simulation
	before the start, pass run_immediately=False,
	then Loader returns a Wesend instance,
	which you can start by start()"""
	_enableCustomSourcesFolder();
	(parsedArgs, extraArgs) = _parseArgs();
	configEd = ConfigEd(parsedArgs.configfile);
	if(parsedArgs.invoke_defaultconfig):
		configEd.writeDefaults();
	if(parsedArgs.invoke_editconfig):
		configEd.edit();
	if(parsedArgs.invoke_printconfig):
		configEd.printConfig();
	config = configEd.getConfig();
	if("_config" in parsedArgs):
		for section, sectionDict in parsedArgs._config.items():
			config[section].update(sectionDict);
	config["resume"] = parsedArgs.resume;
	if(len(extraArgs)>0):
		print("handing over the following command-line arguments to OpenGL: ",
		      " ".join(extraArgs));
	checkSourcesAvailability(config['wesen']['sources']);
	wesend = Wesend(config);
	if(run_immediately):
		wesend.start()
	return wesend;

def _enableCustomSourcesFolder():
	"""Appends to the path a folder where the user can store custom AI code."""
	configroot = join(expanduser("~"),".wesen");
	sourcefolder = join(configroot, "sources");
	if(not exists(configroot)):
		mkdir(configroot);
	if(not exists(sourcefolder)):
		mkdir(sourcefolder);
	sys.path.append(sourcefolder);

def _parseArgs():
	"""returns the result of an ArgumentParser.parse_known_args call"""
	#HINT: If you consider adding an option,
	#      please consider adding a config file option first.
	parser = ArgumentParser(description=STRING_USAGE_DESCRIPTION,
				epilog=STRING_USAGE_EPILOG);
	parser.add_argument('--version', action='version',
			    version='%(prog)s ('+NAMES["PROJECT"]+') '+VERSIONS['PROJECT']);
	parser.add_argument('-c', '--configfile', action='store',
			    dest='configfile',
			    default=DEFAULT_GENERAL_CONFIGFILE,
			    help=STRING_USAGE_CONFIGFILE);
	parser.add_argument('-e', '--editconfig', action='store_true',
			    dest='invoke_editconfig',
			    default=False,
			    help=STRING_USAGE_EDITCONFIG);
	parser.add_argument('--defaultconfig', action='store_true',
			    dest='invoke_defaultconfig',
			    default=False,
			    help=STRING_USAGE_DEFAULTCONFIG);
	parser.add_argument('--printconfig', action='store_true',
			    dest='invoke_printconfig',
			    default=False,
			    help=STRING_USAGE_PRINTCONFIG);
	_addOverwriteBool(parser, 'gui', 'gui', 'enable');
	_addOverwriteBool(parser, 'logger', 'general', 'enablelog');
	parser.add_argument('-l', '--logfile', section='general',
			    dest='logfile',
			    action=_OverwriteConfigAction);
	parser.add_argument('-s', '--sources', section='wesen',
			    dest='sources',
			    action=_OverwriteConfigAction);
	parser.add_argument('-r', '--resume',
			    dest='resume', action='store_true',
			    default=False, help=STRING_USAGE_RESUME);
	return parser.parse_known_args();

def _addOverwriteBool(parser, argName, section, key):
	"""for convenience, adds a mutually exclusive group
	with --enable and --disable argName, to modify [section] key"""
	group = parser.add_mutually_exclusive_group();
	group.add_argument('--enable'+argName, section=section,
			   dest=key,
			   storeValue=True,
			   action=_OverwriteConfigActionBool);
	group.add_argument('--disable'+argName, section=section,
			   dest=key,
			   storeValue=False,
			   action=_OverwriteConfigActionBool);

def checkSourcesAvailability(sourcesList):
	"""imports all source classes which are specified by the config."""
	sources = sourcesList.split(",");
	for source in sources:
		try:
			importlib.import_module(".sources."
						+ source
						+ ".main",
						__package__).WesenSource;
		except ImportError as e:
			print(e);
			print("The source code for one of your AIs could not be loaded: ",
			      source);
			sys.exit();

class _OverwriteConfigAction(Action):
	"""An ArgumentParser Action that stores in a dict
	called _config in the namespace
	which config option should be overwritten by command-line."""
	def __init__(self, option_strings, dest, section, nargs=1):
		helpMessage = (STRING_USAGE_OVERWRITE % (section, dest));
		super(_OverwriteConfigAction, self)\
		    .__init__(option_strings=option_strings,
			      dest=dest, nargs=nargs,
			      const=False, default=None,
			      required=False,
			      help=helpMessage);
		self.section = section;

	def __call__(self, parser, namespace, values, option_string=None):
		if(len(values) != 1):
			raise ValueError("wrong number of values for config option to overwrite: [",
					 self.section, "]",
					 self.dest, "=", ",".join(values));
		else:
			#print("Overwritten config option: [",
			#      self.section, "]",
			#      self.dest, "=",
			#      values[0]);
			if(not "_config" in namespace):
				namespace._config = {};
			if(not self.section in namespace._config.keys()):
				namespace._config[self.section] = {};
			namespace._config[self.section][self.dest] = values[0];
		

class _OverwriteConfigActionBool(_OverwriteConfigAction):
	"""For convenience, storing True/False as specified"""
	def __init__(self, option_strings, dest, section, storeValue=None):
		super(_OverwriteConfigActionBool, self)\
		    .__init__(option_strings=option_strings,
			      dest=dest, section=section,
			      nargs=0);
		self.storeValue = storeValue;

	def __call__(self, parser, namespace, values, option_string=None):
		if(self.storeValue != None):
			values = [self.storeValue];
		super(_OverwriteConfigActionBool, self).__call__(parser, namespace, values);
