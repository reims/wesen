"""Testing which implementation is fastest
for calculating the distance between two 2d points
in the maximum metric.

Mathematics:
dist(p,q) = norm(q-p)
norm(v) = max(abs(v[0]),abs(v[1]))

Output of this program on a Thinkpad T430s:

testing 10 times 200000 calls of each implementation
            implementation -- time consumption in milliseconds
              python_abs_0 --    50
                python_abs --    55
            explicit_abs_0 --    63
            explicit_abs_1 --    78
            python_abs_max --    97
            explicit_abs_2 --   100
                 numpy_abs --   582
  numpy_abs_vector_nparray --  1218
 numpy_linalg_norm_nparray --  2320
          numpy_abs_vector --  2802
         numpy_linalg_norm --  3870


As a consequence, instead of the usual python_abs
or the recommended-on-stackoverflow explicit_abs,
we should use python_abs_0.
Numpy is surprisingly slow.

This time consumption can be roughly explained:
* function calls in python are really expensive
* local variables are cheaper than less local ones
* abs can be implemented more efficiently by forgetting the sign bit,
  instead of comparing against 0
"""

from numpy import array as numpyarray
from numpy import abs as numpyabs
from numpy.linalg import norm as numpylinalgnorm
from numpy import inf as maxmetric
from numpy.random import randint

from timeit import repeat as timeit_repeat


def explicit_abs_0(p, q, radius):
    (x, y) = q
    (a, b) = p
    return ((((a < x) and (x - a <= radius))
             or ((a > x) and (a - x <= radius))
             or ((a == x)))
            and (((b < y) and (y - b <= radius))
                 or ((b > y) and (b - y <= radius))
                 or ((b == y))))


def explicit_abs_1(p, q, radius):
    (x, y) = q
    return ((((p[0] < x) and (x - p[0] <= radius))
             or ((p[0] > x) and (p[0] - x <= radius))
             or ((p[0] == x)))
            and (((p[1] < y) and (y - p[1] <= radius))
                 or ((p[1] > y) and (p[1] - y <= radius))
                 or ((p[1] == y))))


def explicit_abs_2(p, q, radius):
    return ((((p[0] < q[0]) and (q[0] - p[0] <= radius))
             or ((p[0] > q[0]) and (p[0] - q[0] <= radius))
             or ((p[0] == q[0])))
            and (((p[1] < q[1]) and (q[1] - p[1] <= radius))
                 or ((p[1] > q[1]) and (p[1] - q[1] <= radius))
                 or ((p[1] == q[1]))))


def python_abs_0(p, q, radius):
    (px, py) = p
    (qx, qy) = q
    return ((abs(px - qx) <= radius) and
            (abs(py - qy) <= radius))


def python_abs(p, q, radius):
    return ((abs(p[0] - q[0]) <= radius) and
            (abs(p[1] - q[1]) <= radius))


def python_abs_max(p, q, radius):
    return (max(abs(p[0] - q[0]), abs(p[1] - q[1])) <= radius)


def numpy_abs(p, q, radius):
    return ((numpyabs(p[0] - q[0]) <= radius) and
            (numpyabs(p[1] - q[1]) <= radius))


def numpy_abs_vector(p, q, radius):
    return (max(numpyabs([cp - cq for cp, cq in zip(p, q)])) <= radius)


def numpy_linalg_norm(p, q, radius):
    return (numpylinalgnorm([cp - cq for cp, cq in zip(p, q)], ord=maxmetric) <= radius)


def numpy_abs_vector_nparray(pa, qa, radius):
    return (max(numpyabs(pa - qa)) <= radius)


def numpy_linalg_norm_nparray(pa, qa, radius):
    return (numpylinalgnorm(pa - qa, ord=maxmetric) <= radius)

TEST_THESE_ARRAY = (explicit_abs_0, explicit_abs_1, explicit_abs_2,
                    python_abs_0, python_abs, python_abs_max,
                    numpy_abs, numpy_abs_vector, numpy_linalg_norm)
TEST_THESE_NPARRAY = (numpy_abs_vector_nparray, numpy_linalg_norm_nparray)

TEST_WORLDLENGTH = 500
TEST_RADIUS = 30


def some_values():
    d = TEST_WORLDLENGTH // 2
    r = TEST_RADIUS
    return ((randint(-d, d), randint(-d, d)),
            (randint(-d, d), randint(-d, d)),
            randint(r))


def some_values_nparray():
    d = TEST_WORLDLENGTH // 2
    r = TEST_RADIUS
    return (numpyarray([randint(-d, d), randint(-d, d)]),
            numpyarray([randint(-d, d), randint(-d, d)]),
            randint(r))


def test_sophisticated():
    """make sure the functions we test
    all implement the same computation"""
    values = some_values()
    values_nparray = (numpyarray(values[0]),
                      numpyarray(values[1]),
                      values[2])
    result = python_abs(*values)
    for func in TEST_THESE_ARRAY:
        assert result == func(*values)
    for func in TEST_THESE_NPARRAY:
        assert result == func(*values_nparray)


def test_times():
    number = 200000
    repeat = 10
    print("testing", repeat, "times", number, "calls of each implementation")
    setup = ('import testradius;'
             + 'values=testradius.some_values();'
             + 'values_nparray=testradius.some_values_nparray();')
    executionStack = {}
    results = []
    for func in TEST_THESE_ARRAY:
        executionStack[func.__name__]\
            = '(*values)'
    for func in TEST_THESE_NPARRAY:
        executionStack[func.__name__]\
            = '(*values_nparray)'
    #print("testing implementations:\n\t"+"\n\t".join(executionStack.keys()))
    for funcname, values in executionStack.items():
        stmt = 'testradius.' + funcname + values
        min_time = min(
            timeit_repeat(stmt=stmt, setup=setup, number=number, repeat=repeat))
        results.append((funcname, min_time * 1000))
    print("%26s -- time consumption in milliseconds" % ("implementation"))
    for result in sorted(results, key=lambda r: r[1]):
        print("%26s -- %5.0f" % result)

if __name__ == '__main__':
    for _ in range(1000):
        test_sophisticated()
    test_times()
