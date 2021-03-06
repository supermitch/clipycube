"""
Linear algebra is cool.
"""
import math


def rotation(point, axis, theta=None, sign=1):
    """ Rotate a point (or vector) about the origin in 3D space. """
    def Rx(x, y, z, theta):
        return (round(x, 1),
                round(math.cos(theta) * y - math.sin(theta) * z, 1),
                round(math.sin(theta) * y + math.cos(theta) * z, 1))

    def Ry(x, y, z, theta):
        return (round(math.cos(theta) * x + math.sin(theta) * z, 1),
                round(y, 1),
                round(-math.sin(theta) * x + math.cos(theta) * z, 1))

    def Rz(x, y, z, theta):
        return (round(math.cos(theta) * x - math.sin(theta) * y, 1),
                round(math.sin(theta) * x + math.cos(theta) * y, 1),
                round(z, 1))

    R = {0: Rx, 1: Ry, 2: Rz}[axis]  # Select a rotation matrix depending on which axis
    x, y, z = point  # Assumes 3D point or vector
    if theta is None:
        theta = math.pi/2
    return R(x, y, z, sign * theta)  # Calculate our new normal vector


def cross_product(a, b):
    """ Return the angles in (x, y, z) between two vectors, a & b. """
    a1, a2, a3 = a
    b1, b2, b3 = b
    return (a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1)


def dot_product(a, b):
    """ Return dot product between two vectors a & b. """
    a1, a2, a3 = a
    b1, b2, b3 = b
    return a1 * b1 + a2 * b2 + a3 * b3


def length(vector):
    """ Return length of a vector. """
    a, b, c = vector
    return math.sqrt(a ** 2 + b ** 2 + c ** 2)


def angle_between_vectors(a, b):
    """ Return the angle between two vectors. """
    return math.acos(dot_product(a, b) / (length(a) * length(b)))

