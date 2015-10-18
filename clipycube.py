#!/usr/bin/env python

import curses
import itertools
import locale
import logging
import operator
import os
import random
import sys

import algebra
import renderer


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
        self.normal = algebra.rotation(self.normal, axis, sign)
        self.coords = algebra.rotation(self.coords, axis, sign)

    def __repr__(self):
        x, y, z = self.coords
        return 'Sticker({}, {}, {}, {}, {})'.format(x, y, z, self.normal, self.color)


class Cube(object):
    """ A Rubik's cube object. """

    def __init__(self):
        self.normal = (0, 0, 1)  # Our view normal. Doesn't change.
        self.stickers = self.generate()
        self.scramble()

    def generate(self):
        """ Generate our Cube by positioning stickers on all the faces. """
        faces = {
            'left': ([-1.5], range(-1, 2), range(-1, 2), (-1, 0, 0), 'green'),
            'right': ([1.5], range(-1, 2), range(-1, 2), (1, 0, 0), 'blue'),
            'bottom': (range(-1, 2), [-1.5], range(-1, 2), (0, -1, 0), 'red'),
            'top': (range(-1, 2), [1.5], range(-1, 2), (0, 1, 0), 'orange'),
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
        """
        Spin a plane of the cube.
        """
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

    def describe(self):
        """ Describe the cube's entire current layout. """
        print('Cube:')
        for sticker in self.stickers:
            print(sticker)
        print('\n')

    def show(self):
        """ Print the currently displayed face. """
        print('Front:')
        for sticker in self.stickers:
            if sticker.is_visible(self.normal):
                print(sticker)
        print('\n')

    def render(self, screen):
        """ Render ourself. """
        colors = (None, 'red', 'green', 'blue', 'white', 'yellow', 'orange')

        height, width = screen.getmaxyx()
        x_offset, y_offset = int(width/2) - 1, int(height/2) - 1

        block_char = chr(0x2588)  # Python 3 only?
        for sticker in self.stickers:
            if sticker.is_visible(self.normal):
                x, y, z = sticker.coords
                j = int(x + x_offset)
                i = int(y + y_offset)
                pair_number = colors.index(sticker.color)
                screen.attron(curses.color_pair(pair_number))
                screen.addch(i, j, block_char)
                screen.attroff(curses.color_pair(pair_number))


def setup_logging():
    """
    Set up log folder and configure logger.
    """
    root = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(root, 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename='log/clipycube.log', filemode='w', level=logging.DEBUG)


def main_loop(screen):
    """
    Run the main game loop.
    """
    cube = Cube()  # new cube

    screen.box()  # Render window frame
    while True:
        cube.render(screen)
        screen.refresh()

        key = screen.getkey()
        if key == 'x':  # Rotate about x-axis
            cube.rotate(0)
        elif key == 'y':  # Rotate about y-axis
            cube.rotate(1)
        elif key == 'z':  # Rotate about z-axis
            cube.rotate(2)
        elif key == 'j':
            cube.twist('top')
        elif key == 'i':
            cube.twist('middle')  # horizontal
        elif key == 'k':
            cube.twist('bottom')
        elif key == 'h':
            cube.twist('left')
        elif key == 'm':
            cube.twist('center')  # vertical
        elif key == 'l':
            cube.twist('right')
        elif key == 's':
            cube.scramble()
        elif key == 'q':
            break  # Exit the while loop
    screen.erase()  # Avoid flashing reset colours
    screen.refresh()


def game():
    """
    """
    cube = Cube()  # new cube
    cube.show()
    cube.rotate(0)
    cube.show()
    cube.twist('top')
    cube.show()


def curses_gui(screen):
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    curses.use_default_colors()
    curses.start_color()  # Start colour mode
    if not curses.has_colors():
        sys.exit('Terminal does not support colors!')
        # TODO: Fall back to text mode
    else:
        old_colors = renderer.init_colors()

    curses.curs_set(0)  # Hide cursor
    # TODO: @rubiks_colors decorator. Coooool.
    main_loop(screen)

    if curses.has_colors():
        renderer.reset_colors(old_colors)


def main():
    setup_logging()

    if len(sys.argv) > 1 and sys.argv[1] == 'ui':
        curses.wrapper(curses_gui)
    else:
        game()


if __name__ == '__main__':
    main()

