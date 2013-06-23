#! /usr/bin/python3

from src.Wesen.wesend import Wesend;
import cProfile;
import pstats;
cProfile.run('Wesend()', "profile.stats");
print("If you experience problems with profiling, configure wesen to run without GUI first.");

stats = pstats.Stats('profile.stats')

# Clean up filenames for the report
stats.strip_dirs()

# Sort the statistics by the cumulative time spent in the function
stats.sort_stats('cumulative')

stats.print_stats()