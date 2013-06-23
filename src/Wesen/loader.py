#! /usr/bin/python3

"""Copyright 2003-2013 by Konrad Voelkel and Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit https://github.com/reims/wesen for versions > 2013
or http://wesen.sourceforge.net for old versions of 2003,2004."""

from .wesend import Wesend;
from .defaults import DEFAULT_GENERAL_CONFIGFILE, DEFAULT_GENERAL_CONFIGFILE_PROFILE;
from .strings import STRING_ERROR_NOTSAMEPATH, STRING_USAGE_LOADER;
from .configed import ConfigEd;
from optparse import OptionParser;
from os import execv, environ, mkdir;
from os.path import exists, join, dirname, expanduser;
import sys;

class Loader(object):
	"""The Loader determines which configfile to use and interprets command-line arguments. It then runs a Wesend instance."""

	def __init__(self):
		self.main();

	def main(self):
		"""control flow:
		if --help was given, print the usage string and quit
		check whether config file was supplied in args
		 check whether it exists
		  if, use it and continue parsing commandline
		  if not, cry and quit
		 if no config file supplied, use default location
		  if exists, use it and continue parsing commandline
		  if not, create it (write defaults to it) and then use it and continue parsing
		check whether the option to edit the config was given
		 if, launch the editor
		 if not, see if the option to write default config was given,
		  write the default config to the configfile in use
		read the configfile we decided to use
		manipulate the config info according to
		 --(enable|disable)(gui|logger) and --logfile and --sources
		run wesend with this config and remaining args (for OpenGL).
		"""
		#TODO rewrite following code according to flow described above
		configroot = join(expanduser("~"),".wesen");
		sourcefolder = join(configroot, "sources");
		if(not exists(configroot)):
			mkdir(configroot);
		if(not exists(sourcefolder)):
			mkdir(sourcefolder);
		sys.path.append(sourcefolder);
		args = sys.argv;
		if len(args) >= 2:
			argument = args[1];
			if argument == "c":
				from .configed import ConfigEd;
				if len(args)==4:
					configEd=ConfigEd(args[2]);
				else:
					configEd=ConfigEd(DEFAULT_GENERAL_CONFIGFILE);
					configEd.edit();
				if "-e" in args or "--edit" in args:
					configEd.edit();
				if "-d" in args or "--defaults" in args:
					configEd.writeDefaults();
				if "-g" in args or "--get" in args:
					configEd.printConfig();
			elif argument == "d":
				wesend = Wesend(self.readConfig());
			else:
				print(STRING_USAGE_LOADER);
		else:
			print(STRING_USAGE_LOADER);

	def readConfig(self, configfile=DEFAULT_GENERAL_CONFIGFILE):
		return ConfigEd(configfile).getConfig();
