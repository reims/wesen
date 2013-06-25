#! /usr/bin/python3

from src.Wesen.loader import Loader;
from cProfile import Profile;
from time import perf_counter;
from pstats import Stats;
import sys;

print("You can supply an alternative config file on the command-line");
print("You can stop profiling by Ctrl+C");

sys.argv.append('--disablegui');
sys.argv.append('--disablelog');
pr = Profile(perf_counter);
pr.run('Loader()');

stats = Stats(pr)

stats.sort_stats('tottime')
stats.print_stats(20)
