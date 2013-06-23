#! /usr/bin/python3

from src.Wesen.loader import Loader;
import cProfile;
import pstats;
import sys;

print("You can supply an alternative config file on the command-line");
print("You can stop profiling by Ctrl+C");

sys.argv.append('d'); #TODO change to '--disablegui' after Loader command-line parser re-write
cProfile.run("Loader()", "profile.stats");

stats = pstats.Stats('profile.stats')

# Clean up filenames for the report
stats.strip_dirs()

# Sort the statistics by the cumulative time spent in the function
stats.sort_stats('cumulative')

stats.print_stats()
