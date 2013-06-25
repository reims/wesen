"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from numpy.random import randint;
from math import copysign;

def getRandomPosition(length):
	"""returns a random n-dimensional position."""
	return [randint(0,length-1), randint(0,length-1)];

def getRandomPositionInRadius(position, radius, length):
	"""x + random(-radius,+radius)"""
	return [(length + pc + randint(-radius,radius)) % length for pc in position];

def signum(number):
	return -1 if number < 0 else 1 if number > 0 else 0;

def getShortestTranslation(a, b, length):
	return [min(c,-1*copysign(length-c,c),key=abs) for c in [(bc-ac) % length for (ac,bc) in zip(a,b)]];

def getDistInMaxMetric(a, b, length):
	return abs(max(getShortestTranslation(a,b,length), key=abs));
















