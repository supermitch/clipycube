import algebra


class Sticker(object):
    """
    A sticker object. There are 9 on each face of the cube.
    Think of it like a sprite that can be moved and rendered.
    """
    def __init__(self, x, y, z, normal, color):
        """ Initialize position, orientation, and color. """
        self.coords = x, y, z
        self.normal = normal  # Normal vector
        self.color = color

    def is_visible(self, vector):
        """ Is this sticker visible along a given vector. """
        return self.normal == vector

    def rotate(self, axis, sign=1):
        """ Rotate this sticker in 3D space about the origin. """
        self.normal = algebra.rotation(self.normal, axis, sign=sign)
        self.coords = algebra.rotation(self.coords, axis, sign=sign)

    def __repr__(self):
        x, y, z = self.coords
        return 'Sticker({}, {}, {}, {}, {})'.format(x, y, z, self.normal, self.color)


