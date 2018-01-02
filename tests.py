import math
import numpy


def direction(x, y):
    return numpy.sign(y)


def left_wheel(x, y):
    """Takes normalized direction vector (x,y) as input."""
    if numpy.linalg.norm((x, y)) < 1:
        return 0

    if direction(x, y) > 0:
        return direction(x, y) * abs(y)
    elif direction(x, y) < 0:
        return direction(x, y) * numpy.linalg.norm((x, y))
    else:
        return x


def right_wheel(x, y):
    if numpy.linalg.norm((x, y)) < 1:
        return 0

    if direction(x, y) < 0:
        return direction(x, y) * abs(y)
    elif direction(x, y) > 0:
        return direction(x, y) * numpy.linalg.norm((x, y))
    else:
        return -x


def wheels(x, y):
    if numpy.linalg.norm((x, y)) < 1:
        return (0, 0)

    d = direction(x, y)
    if d > 0:
        left = direction(x, y) * abs(y)
        right= direction(x, y) * numpy.linalg.norm((x, y))
    elif d < 0:
        left = direction(x, y) * numpy.linalg.norm((x, y))
        right= direction(x, y) * abs(y)
    else:
        left = x
        right = -x

    return (left, right)



if __name__ == "__main__":
    def test_wheels(x, y):
        (vl, vr) = wheels(x, y)
        # vr = right_wheel(x, y)
        # d = direction(x, y)
        #print "direction(", x, ",", y, ") ->", d
        print "wheels(", x, ",", y, ") ->", vl, ",", vr

    test_wheels(0, 0)
    test_wheels(0, 100)
    test_wheels(-70.71, 70.71)
    test_wheels(-25, 25)
    test_wheels(-100, 10)
    test_wheels(-100, 0)
    test_wheels(-100, -10)
    test_wheels(-70.71, -70.71)
    test_wheels(-25, -25)

    test_wheels(0, -100)
    test_wheels(70.71, 70.71)
    test_wheels(25, 25)
    test_wheels(100, 10)
    test_wheels(100, 0)
    test_wheels(100, -10)
    test_wheels(70.71, -70.71)
    test_wheels(25, -25)

