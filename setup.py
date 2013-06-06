#! /usr/bin/env python

from distutils.core import setup;

SUMMARY = """
Wesen is german for something alife.
You can program the instincts of a species -
and let them fight against others (not only by fight but by best survival).
This way, you can do nice programming contests and learn python by the way!
"""

CLASSIFIERS = """
Development Status :: 4 - Beta
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Simulation
"""

def main():
	setup(name="wesen", version="0.5.02", license="GNU GPL",
              author="Konrad Voelkel, Reimer Backhaus", author_email="wesen@gekonnt.de",       url="http://www.sourceforge.net/projects/wesen",       description="programmable life simulation",       package_dir={"Wesen":"src"}, packages=["Wesen", "Wesen.objects", "Wesen.gui", "Wesen.sources", "Wesen.sources.DrunkenSailor", "Wesen.sources.Nightwatch", "Wesen.sources.Scanner", "Wesen.sources.WindlePoons", "Wesen.sources.Manual"], scripts = ["wesen", "postinstall_win32.py"], long_description = SUMMARY.strip(), classifiers = filter(None, CLASSIFIERS.split("\n")), platforms = ["Many"])#, maintainer = "Konrad Voelkel, Reimer Backhaus", maintainer_email = "wesen@gekonnt.de");

if(__name__ == "__main__"):
	main();