#! /bin/env python

from distutils.sysconfig import get_python_lib as getpythonpath;
from os.path import join;
import sys;

def Install():
	print "Installing ...";
	desktop = get_special_folder_path("CSIDL_DESKTOPDIRECTORY");
	iconpath = "";
	pythonpath = getpythonpath();
	launcherpath = join(pythonpath, "Wesen/loader.py");
	linkpath = join(desktop, "Wesen.lnk");
	create_shortcut(launcherpath, "run wesen", linkpath, "dd > NULL")#, "", iconpath);

def Deinstall():
	print "Deinstalling ...";
	print "warning: deinstallation not implemented yet";

def main():
	if(len(sys.argv) < 2):
		print "critical error: not enough arguments";
		sys.exit();
	print "running post-install script (win32)";
	mode = (sys.argv[1][1] != "r");
	if(mode == 0):
		Deinstall();
	else:
		Install();
	print "done.";

main();