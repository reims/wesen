"""Copyright 2003 by Konrad Voelkel Reimer Backhaus.
This program is distributed under the terms of the GNU General Public License.
visit http://www.sourceforge.net/projects/wesen or
http://wesen.sourceforge.net for newer versions."""

from .definition import DIMENSIONS;
from random import randint;

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
	return [((position[0] + signum(direction[0]) + length) % length),
                ((position[1] + signum(direction[1]) + length) % length)];

def positionToDirection(position, newposition, length):
	"""returns the direction from one point to another one."""
	direction = [];
	for i in range(DIMENSIONS):
		if(newposition[i] < position[i]):
			direction.append(-1);
		elif(newposition[i] > position[i]):
			direction.append(1);
		else:
			direction.append(0);
	return direction;

def getZeroPosition():
	#return [0 for i in range(DIMENSIONS)];
	return [0, 0];


















