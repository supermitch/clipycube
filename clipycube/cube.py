import operator
import random

from sticker import Sticker


class Cube(object):
    """ A Rubik's cube object. """

    def __init__(self):
        self.stickers = self.generate()
        self.scramble()

    def generate(self):
        """ Generate our Cube by positioning stickers on all the faces. """
        faces = {
            'left': ([-1.5], range(-1, 2), range(-1, 2), (-1, 0, 0), 'blue'),
            'right': ([1.5], range(-1, 2), range(-1, 2), (1, 0, 0), 'green'),
            'bottom': (range(-1, 2), [-1.5], range(-1, 2), (0, -1, 0), 'orange'),
            'top': (range(-1, 2), [1.5], range(-1, 2), (0, 1, 0), 'red'),
            'back': (range(-1, 2), range(-1, 2), [-1.5], (0, 0, -1), 'yellow'),
            'front': (range(-1, 2), range(-1, 2), [1.5], (0, 0, 1), 'white'),
        }
        stickers = []
        for xs, ys, zs, normal, color in faces.values():
            for x in xs:
                for y in ys:
                    for z in zs:
                        stickers.append(Sticker(x, y, z, normal, color))
        return stickers

    def rotate(self, axis, sign=1):
        """ Reorient our cube by rotation about an axis. """
        for sticker in self.stickers:
            sticker.rotate(axis, sign)

    def twist(self, plane, sign=1):
        """ Spin a plane of the cube. """
        twist = {  # plane: (comparison function, axis),
            'top': (operator.gt, 1),
            'middle': (operator.eq, 1),
            'bottom': (operator.lt, 1),
            'right': (operator.gt, 0),
            'center': (operator.eq, 0),
            'left': (operator.lt, 0),
        }
        comparison, axis = twist[plane]
        for sticker in self.stickers:
            if comparison(sticker.coords[axis], 0):  # Only rotate stickers in the selected plane
                sticker.rotate(axis, sign)

    def scramble(self):
        """ Scramble our faces. """
        planes = ['top', 'middle', 'bottom', 'right', 'center', 'left']
        for _ in range(3000):
            self.twist(random.choice(planes))

    def solve(self):
        """ Put the cube in the initial ('solved') state. """
        self.stickers = self.generate()

    def describe(self):
        """ Describe the cube's entire current layout. """
        print('Cube:')
        for sticker in self.stickers:
            print(sticker)
        print('\n')

    def show(self, normal=(0, 0, 1)):
        """ Print the stickers facing the given normal vector. """
        print('Normal: {}'.format(normal))
        for sticker in self.stickers:
            if sticker.is_visible(normal):
                print(sticker)

