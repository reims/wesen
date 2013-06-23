"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from .definition import DIMENSIONS;
from random import randint;
from math import copysign;

def getRandomPosition(length):
	"""returns a random n-dimensional position."""
	#return [randint(0,length-1) for i in range(DIMENSIONS)];
	return [randint(0,length-1), randint(0,length-1)]

def getRandomPositionInRadius(pos, radius, length):
	"""x + random(-radius,+radius)"""
	#return [(length + pos[i] + randint(-radius,radius)) % length for i in range(DIMENSIONS)];
	return [(length + pos[0] + randint(-radius,radius)) % length, (length + pos[1] + randint(-radius,radius)) % length];

def signum(number):
	if(number < 0): return -1;
	elif(number > 0): return 1;
	else: return 0;

def getNewPosition(position, direction, length):
	"""returns the position resulting from going into "direction" from "position"."""
	#return [((position[i] + signum(direction[i]) + length) % length) for i in range(DIMENSIONS)]
	return [((position[0] + direction[0]) % length),
                ((position[1] + direction[1]) % length)];

def positionToDirection(position, newposition):
	"""returns the direction from one point to another one."""
	return [signum(c-p) for (c,p) in zip(newposition, position)];
#	for i in range(DIMENSIONS):
#		if(newposition[i] < position[i]):
#			direction.append(-1);
#		elif(newposition[i] > position[i]):
#			direction.append(1);
#		else:
#			direction.append(0);
#	return direction;

def getZeroPosition():
	#return [0 for i in range(DIMENSIONS)];
	return [0, 0];

def getShortestTranslation(a, b, length):
	a = [c % length for c in a];
	b = [c % length for c in b];
	return [min(b[i]-a[i], -1*copysign(length-abs(b[i]-a[i]),b[i]-a[i]), key=abs) for i in range(len(a))];


def getDistInMaxMetric(a, b, length):
	return abs(max(getShortestTranslation(a,b,length), key=abs));
















