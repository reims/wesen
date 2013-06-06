#! /usr/bin/python

"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from defaults import DEFAULT_GENERAL_CONFIGFILE, DEFAULT_GENERAL_CONFIGFILE_PROFILE;
from strings import STRING_ERROR_NOTSAMEPATH, STRING_USAGE_LOADER;
from optparse import OptionParser;
from os import execv, environ, mkdir;
from sys import argv;
from os.path import exists, join, dirname, expanduser;
import sys;

class Loader(object):
	"""class which parses the given arguments and starts the right script."""

	def execwesen(self, directory, filename, args):
		execv(join(directory, filename), [filename]+args);

	def __init__(self):
		self.main();

	def main(self, *arguments):
		"""starts the right scripts with the given arguments"""
		configroot = join(expanduser("~"),".wesen");
		sourcefolder = join(configroot, "sources");
		if(not exists(configroot)):
			mkdir(configroot);
		if(not exists(sourcefolder)):
			mkdir(sourcefolder);
		sys.path.append(sourcefolder);
		if(len(arguments) == 0):
			args = argv;
		else:
			args = arguments[0];
		if len(args) >= 2:
			argument = args[1];
			if argument == "c":
				from configed import ConfigEd;
				if len(args)==4:
					configEd=ConfigEd(args[2]);
				else:
					configEd=ConfigEd(DEFAULT_GENERAL_CONFIGFILE);
					configEd.edit();
				if "-e" in args or "--edit" in args:
					configEd.edit();
				if "-d" in args or "--defaults" in args:
					configEd.writeDefaults();
				if "-p" in args or "--profile" in args:
					configEd.writeProfileConfig();
				if "-g" in args or "--get" in args:
					configEd.printConfig();
			elif argument == "d":
				from wesend import Wesend;
				wesend = Wesend();
			elif argument == "h":
				print("help")
			elif argument == "cd":
				self.main([args[0], "c", DEFAULT_GENERAL_CONFIGFILE, "-d"]);
			elif argument == "cp":
				self.main([args[0], "c", DEFAULT_GENERAL_CONFIGFILE_PROFILE, "-p"]);
			elif argument == "dd":
				self.main([args[0],"cd"]);
				self.main([args[0],"d"]);
			else:
				print(STRING_USAGE_LOADER);
		else:
			print(STRING_USAGE_LOADER);
			self.main([args[0],"dd"]);

if(__name__ == "__main__"):
	Loader();
