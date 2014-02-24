"""These are some helping functions,
that come handy in writing an AI.
In future, this code might move elsewhere."""

from numpy.random import randint
from math import copysign


def getRandomPosition(length):
    """returns a random n-dimensional position."""
    return [randint(0, length - 1), randint(0, length - 1)]


def getRandomPositionInRadius(position, radius, length):
    """x + random(-radius,+radius)"""
    return [(length + pc + randint(-radius, radius)) % length
            for pc in position]


def signum(number):
    """return the sign +-1 or 0 if 0"""
    return -1 if number < 0 else 1 if number > 0 else 0


def getShortestTranslation(a, b, length):
    """takes ((ax,ay),(bx,by),length),
    computes shortest vector from a to b."""
    return [min(c, -1 * copysign(length - c, c), key=abs)
            for c in [(bc - ac) % length for (ac, bc) in zip(a, b)]]


def getDistInMaxMetric(a, b, length):
    """takes ((ax,ay),(bx,by),length),
    computes distance from a to b."""
    return abs(max(getShortestTranslation(a, b, length), key=abs))
