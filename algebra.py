"""
Linear algebra is cool.
"""
import math


def rotation(point, axis, sign=1):
    """
    Rotate a point (or vector) about the origin in 3D space.
    """
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
    R = {'x': Rx, 'y': Ry, 'z': Rz}[axis]  # Select a rotation matrix
    theta = sign * math.pi / 2  # Always 90 degrees
    x, y, z = point  # Assumes 3D point or vector
    return R(x, y, z, theta)  # Calculate our new normal vector

