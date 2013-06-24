#! /usr/bin/python3

"""Copyright 2003-2013 by Konrad Voelkel and Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit https://github.com/reims/wesen for versions > 2013
or http://wesen.sourceforge.net for old versions of 2003,2004."""

from .definition import NAMES, VERSIONS;
from .defaults import DEFAULT_GENERAL_CONFIGFILE, DEFAULT_GENERAL_LOGFILE;
from .strings import *;
from .configed import ConfigEd;
from .wesend import Wesend;
from argparse import ArgumentParser, Action;
from os import execv, environ, mkdir;
from os.path import exists, join, dirname, expanduser;
import importlib;
import sys;

class Loader(object):
	"""The Loader determines which configfile to use and interprets command-line arguments. It then runs a Wesend instance."""

	def __init__(self):
		self.main();

	def main(self):
		self.enableCustomSourcesFolder();
		(parsedArgs, extraArgs) = self.parseArgs();
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
		if(len(extraArgs)>0):
			print("handing over the following command-line arguments to OpenGL: ", " ".join(extraArgs));
		self.checkSourcesAvailability(config['wesen']['sources']);
		Wesend(config);

	def enableCustomSourcesFolder(self):
		configroot = join(expanduser("~"),".wesen");
		sourcefolder = join(configroot, "sources");
		if(not exists(configroot)):
			mkdir(configroot);
		if(not exists(sourcefolder)):
			mkdir(sourcefolder);
		sys.path.append(sourcefolder);

	def parseArgs(self):
		parser = ArgumentParser(description=STRING_USAGE_DESCRIPTION,
					epilog=STRING_USAGE_EPILOG);
		parser.add_argument('--version', action='version',
				    version='%(prog)s ('+NAMES["PROJECT"]+') '+VERSIONS['PROJECT']);
		parser.add_argument('-c', '--configfile', action='store', dest='configfile',
				    default=DEFAULT_GENERAL_CONFIGFILE,
				    help=STRING_USAGE_CONFIGFILE);
		parser.add_argument('-e', '--editconfig', action='store_true', dest='invoke_editconfig',
				    default=False,
				    help=STRING_USAGE_EDITCONFIG);
		parser.add_argument('--defaultconfig', action='store_true', dest='invoke_defaultconfig',
				    default=False,
				    help=STRING_USAGE_DEFAULTCONFIG);
		parser.add_argument('--printconfig', action='store_true', dest='invoke_printconfig',
				    default=False,
				    help=STRING_USAGE_PRINTCONFIG);
		group = parser.add_mutually_exclusive_group();
		group.add_argument('--enablegui', section='gui', dest='enable',
				    storeValue=True,
				    action=OverwriteConfigActionBool);
		group.add_argument('--disablegui', section='gui', dest='enable',
				    storeValue=False,
				    action=OverwriteConfigActionBool);
		group = parser.add_mutually_exclusive_group();
		group.add_argument('--enablelogger', section='general', dest='enablelog',
				    storeValue=True,
				    action=OverwriteConfigActionBool);
		group.add_argument('--disablelogger', section='general', dest='enablelog',
				    storeValue=False,
				    action=OverwriteConfigActionBool);
		parser.add_argument('-l', '--logfile', section='general', dest='logfile',
				    action=OverwriteConfigAction);
		parser.add_argument('-s', '--sources', section='wesen', dest='sources',
				    action=OverwriteConfigAction);
		return parser.parse_known_args();

	def checkSourcesAvailability(self, sourcesList):
		"""imports all source classes which are specified by the config."""
		sources = sourcesList.split(",");
		for source in sources:
			try:
				sourceClass = importlib.import_module(".sources."+source+".main", __package__).WesenSource;
			except ImportError as e:
				print(e);
				print("The source code for one of your AIs could not be loaded: ", source);
				sys.exit();

class OverwriteConfigAction(Action):
	def __init__(self, option_strings, dest, section, nargs=1):
		super(OverwriteConfigAction, self).__init__(option_strings=option_strings, dest=dest, nargs=nargs, const=False, default=None, required=False, help=STRING_USAGE_OVERWRITE);
		self.section = section;

	def __call__(self, parser, namespace, values, option_string=None):
		if(len(values) != 1):
			raise ValueError("wrong number of values for config option to overwrite: [",self.section, "]", self.dest, "=",",".join(values));
		else:
			print("Overwritten config option: [",self.section, "]", self.dest, "=", values[0]);
			if(not "_config" in namespace):
				namespace._config = dict();
			if(not self.section in namespace._config.keys()):
				namespace._config[self.section] = dict();
			namespace._config[self.section][self.dest] = values[0];
		

class OverwriteConfigActionBool(OverwriteConfigAction):
	def __init__(self, option_strings, dest, section, storeValue=None):
		super(OverwriteConfigActionBool, self).__init__(option_strings=option_strings, dest=dest, section=section, nargs=0);
		self.storeValue = storeValue;

	def __call__(self, parser, namespace, values, option_string=None):
		if(self.storeValue != None):
			values = [self.storeValue];
		super(OverwriteConfigActionBool, self).__call__(parser, namespace, values);
