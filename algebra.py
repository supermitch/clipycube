"""
Linear algebra is cool.
"""
import math


def rotation(point, axis, sign=1):
    """
    Rotate a point (or vector) about the origin in 3D space.
    """
    def Rx(x, y, z, theta):
        return (int(x),
                int(math.cos(theta) * y - math.sin(theta) * z),
                int(math.sin(theta) * y + math.cos(theta) * z))

    def Ry(x, y, z, theta):
        return (int(math.cos(theta) * x + math.sin(theta) * z),
                int(y),
                int(-math.sin(theta) * x + math.cos(theta) * z))

    def Rz(x, y, z, theta):
        return (int(math.cos(theta) * x - math.sin(theta) * y),
                int(math.sin(theta) * x + math.cos(theta) * y),
                int(z))
    R = {'x': Rx, 'y': Ry, 'z': Rz}[axis]  # Select a rotation matrix
    theta = sign * math.pi / 2  # Always 90 degrees
    x, y, z = point  # Assumes 3D point or vector
    return R(x, y, z, theta)  # Calculate our new normal vector

