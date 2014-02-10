"""Testing which implementation is fastest
for getting a "range" in the sense of Wesen

A "range" is a dictionary of type id:worldobject
with all objects (from some iterator)
in a given radius around a given position,
matching a given condition.

Output of this program on a Thinkpad T430s:

testing with condition Aged
testing 40 times 3000 calls of each implementation
                          implementation -- time consumption in milliseconds
               getRangeIterator_1_c_last --   303
                    getRangeIterator_3_c --   307
                    getRangeIterator_1_c --   332
              getRangeIterator_1_c_force --   334
                      getRangeIterator_1 --   339
testing with condition Lambda_True
testing 40 times 3000 calls of each implementation
                          implementation -- time consumption in milliseconds
                      getRangeIterator_1 --   331
              getRangeIterator_1_c_force --   335
                    getRangeIterator_1_c --   346
               getRangeIterator_1_c_last --   497
                    getRangeIterator_3_c --   888
testing with condition Food
testing 40 times 3000 calls of each implementation
                          implementation -- time consumption in milliseconds
                    getRangeIterator_1_c --   327
              getRangeIterator_1_c_force --   335
                      getRangeIterator_1 --   342
               getRangeIterator_1_c_last --   607
                    getRangeIterator_3_c --  1010
testing with condition Wesen
testing 40 times 3000 calls of each implementation
                          implementation -- time consumption in milliseconds
               getRangeIterator_1_c_last --   313
                    getRangeIterator_3_c --   326
                      getRangeIterator_1 --   326
                    getRangeIterator_1_c --   332
              getRangeIterator_1_c_force --   334


We see that the variants without _c (which just doesn't check the condition)
are no better than the variants with _c.
We see that all implementations behave
very similar for conditions Aged and Wesen
(which match only few objects)
and quite different for conditions True and Food,
where we have three "winners":
 getRangeIterator_1         -- 331 or 342
 getRangeIterator_1_c_force -- 335
 getRangeIterator_1_c       -- 346 or 327
and the _1_c_force variant arguably has clearest code,
which makes it our choice.
"""

from numpy.random import randint

from src.Wesen.loader import Loader
from src.Wesen.defaults import DEFAULT_CONFIGFILE

from sys import argv
from timeit import repeat as timeit_repeat

def getRangeIterator_3_c(objectIterator, position, radius, condition=None):
    (x, y) = position;
    return ((i, o)
            for (i, o, px, py) in ((i, o, p[0], p[1])
                                   for (i, o, p) in ((i, o, o.position)
                                                     for (i, o) in objectIterator
                                                     if (condition is None or condition(o))))
            if(abs(x - px) <= radius and
               abs(y - py) <= radius));

def getRangeIterator_3(objectIterator, position, radius, condition=None):
    (x, y) = position;
    return ((i, o)
            for (i, o, px, py) in ((i, o, p[0], p[1])
                                   for (i, o, p) in ((i, o, o.position)
                                                     for (i, o) in objectIterator))
            if(abs(x - px) <= radius and
               abs(y - py) <= radius));

def getRangeIterator_2(objectIterator, position, radius, condition=None):
    (x, y) = position;
    return ((i, o)
            for (i, o, p) in ((i, o, o.position)
                              for (i, o) in objectIterator)
            if(abs(x - p[0]) <= radius and
               abs(y - p[1]) <= radius));

def getRangeIterator_1(objectIterator, position, radius, condition=None):
    (x, y) = position;
    return ((i, o)
            for (i, o) in objectIterator
            if(abs(x - o.position[0]) <= radius and
               abs(y - o.position[1]) <= radius));

def getRangeIterator_1_c(objectIterator, position, radius, condition=None):
    (x, y) = position;
    return ((i, o)
            for (i, o) in objectIterator
            if(abs(x - o.position[0]) <= radius and
               abs(y - o.position[1]) <= radius and
               (condition is None or condition(o))));

def getRangeIterator_1_c_force(objectIterator, position, radius, condition):
    (x, y) = position;
    return ((i, o)
            for (i, o) in objectIterator
            if(abs(x - o.position[0]) <= radius and
               abs(y - o.position[1]) <= radius and
               (condition is None or condition(o))));

def getRangeIterator_1_c_force_strongly(objectIterator, position, radius, condition):
    #XXX does not work with condition=None!
    (x, y) = position;
    return ((i, o)
            for (i, o) in objectIterator
            if(abs(x - o.position[0]) <= radius and
               abs(y - o.position[1]) <= radius and
               condition(o)));

def getRangeIterator_1_c_last(objectIterator, position, radius, condition=None):
    (x, y) = position;
    return ((i, o)
            for (i, o) in objectIterator
            if((condition is None or condition(o)) and
               abs(x - o.position[0]) <= radius and
               abs(y - o.position[1]) <= radius));

TEST_THESE = (#getRangeIterator_3,
              #getRangeIterator_2,
              getRangeIterator_1,
              getRangeIterator_3_c,
              getRangeIterator_1_c,
              getRangeIterator_1_c_last,
              getRangeIterator_1_c_force)

TEST_RADIUS = 40;
TEST_NUMBER = 300;
TEST_REPEAT = 40;

SETUP = ('import testrange;'
         + '(worldobjects, worldlength) = testrange.initWorld();'
         + 'objects = worldobjects;'
         + 'position = testrange.some_position(worldlength);'
         + 'radius = testrange.TEST_RADIUS;'
         + 'values = (objects, position, radius, condition);')

SETUP_WITH_CONDITION_NONE = ('condition = None;' + SETUP)
SETUP_WITH_CONDITION_LAMBDA_TRUE = ('condition = lambda x : True;' + SETUP)
SETUP_WITH_CONDITION_FOOD = ('condition = lambda o : o.objectType == "food";'
                             + SETUP) # matches many objects
SETUP_WITH_CONDITION_WESEN = ('condition = lambda o : o.objectType == "wesen";'
                             + SETUP) # matches few objects
SETUP_WITH_CONDITION_AGE = ('condition = lambda o : o.age >= 10;'
                             + SETUP) # matches no objects

SETUPS_WITH_CONDITIONS = {#"None":SETUP_WITH_CONDITION_NONE,
                          "Lambda_True":SETUP_WITH_CONDITION_LAMBDA_TRUE,
                          "Food":SETUP_WITH_CONDITION_FOOD,
                          "Wesen":SETUP_WITH_CONDITION_WESEN,
                          "Aged":SETUP_WITH_CONDITION_AGE}

def initWorld():
    wesend = Loader(run_immediately=False)
    world = wesend.world
    worldobjects = world.objects.items()
    worldlength = world.infoAllWorld["world"]["length"]
    return (worldobjects, worldlength)

def some_position(worldlength):
    d = worldlength - 1
    return (randint(0,d), randint(0,d))

def test_sophisticated():
    """make sure the functions we test
    all implement the same computation"""
    (worldobjects, worldlength) = initWorld()
    values = (worldobjects, some_position(worldlength), TEST_RADIUS)
    result = list(getRangeIterator_3_c(*values))
    for condition in [None, lambda x : True]:
        for func in TEST_THESE:
                assert result == list(func(*values, condition=condition))

def test_times_generic(setup):
    number = TEST_NUMBER
    repeat = TEST_REPEAT
    print("testing",repeat,"times",number,"calls of each implementation")
    executionStack = {}
    results = []
    for func in TEST_THESE:
        executionStack[func.__name__]\
            = '(*values)'
    for funcname, values in executionStack.items():
        stmt = 'list(testrange.' + funcname + values + ')'
        min_time = min(timeit_repeat(stmt=stmt, setup=setup, number=number, repeat=repeat))
        results.append((funcname, min_time*1000))
    print("%40s -- time consumption in milliseconds" % ("implementation"))
    for result in sorted(results, key = lambda r : r[1]):
        print("%40s -- %5.0f" % result)

def test_times():
    for title, setup in SETUPS_WITH_CONDITIONS.items():
        print("testing with condition",title)
        test_times_generic(setup)

if __name__ == '__main__':
    argv.append("--disablegui")
    for _ in range(10):
        test_sophisticated()
    test_times()
