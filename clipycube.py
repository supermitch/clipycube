#!/usr/bin/env python

import collections
import curses
import datetime
import itertools
import locale
import logging
import math
import random
import sys


# Faces
TOP = 'top'
BOTTOM = 'bottom'
FRONT = 'front'
BACK = 'back'
LEFT = 'left'
RIGHT = 'right'

# Twist planes
MIDDLE = 'middle'
CENTER = 'center'
# Also TOP, BOTTOM, LEFT & RIGHT


class Sticker(object):
    """ A block's sticker object. """
    def __init__(self, x, y, z, normal, color):
        self.coords = x, y, z
        self.normal = normal  # Normal vector
        self.color = color

    @property
    def is_visible(self, vector):
        """ Is this sticker visible along a given vector. """
        return self.normal == vector

    def rotate(self, axis, sign):
        """ Rotate this sticker in 3D space about the origin. """
        self.normal = algebra.rotation(self.normal, axis, sign)
        self.coords = algebra.rotation(self.coords, axis, sign)


class Cube(object):
    """ A Rubik's cube object. """
    def __init__(self):
        self.face_labels = (TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT)
        self.normal = (0, 0, -1)  # Current view vector
        self.stickers = self.generate()
        self.scramble()

    def generate(self):
        """ Generate our Cube. """
        stickers = [[[None] * 3 for _ in range(3)] for _ in range(3)]
        for x, y, z in itertools.product(range(3), repeat=3):
            if x == 0:
                vector = (-1, 0, 0)
                color = 'green'
            elif x == 2:
                vector = (1, 0, 0)
                color = 'blue'
            if y == 0:
                vector = (0, -1, 0)
                color = 'red'
            elif y == 2:
                vector = (0, 1, 0)
                color = 'orange'
            if z == 0:
                vector = (0, 0, -1)
                color = 'yellow'
            elif z == 2:
                vector = (0, 0, 1)
                color = 'white'
            stickers[x][y][z] = Sticker(x, y, z, vector, color)
        return stickers

    def rotate(self, axis, sign=1):
        """ Reorient our facing vector by rotation about an axis. """
        self.normal = algebra.rotation(self.normal, axis, sign=sign)
        # Reposition stickers
        for x, y, z in itertools.product(range(3), repeat=3):
            sticker = self.stickers[x][y][z]
            sticker.rotate(axis, sign=sign)

    def twist(self, plane):
        """
        Spin a plane of the cube.
        """
        if plane == TOP:
            # Assuming view is front (0, 0, 1)
            # Right becomes front
            # Back becomes right
            # Left becomes back
            # Front becomes left
            # So each part of each face is rotated about the y-axis
            # The top pane is rotated through 90 
            # The bottom 2 panes remain untouched
            pass

    @property
    def view(self):
        """ Return our facing view, given our facing vector. """
        return {
            (0, 0, 1): FRONT,
            (1, 0, 0): RIGHT,
            (0, 1, 0): TOP,
            (0, 0, -1): BACK,
            (-1, 0, 0): LEFT,
            (0, -1, 0): BOTTOM,
        }.get(self.normal, None)

    def scramble(self):
        """ Scramble our faces. """
        pass

    def describe(self):
        """ Describe the cube's current layout. """
        for name, face in self.faces.items():
            print(name, face)

    def show(self):
        """ Print the currently displayed face. """
        print(self.view, self.faces[self.view])

    def render(self, screen):
        """ Render ourself. """
        colors = ('red', 'green', 'blue', 'white', 'yellow', 'orange')

        height, width = screen.getmaxyx()
        x_offset, y_offset = int(width/2), int(height/2)

        block = chr(0x2588)  # Python 3 only?
        for x, y, z in itertools.product(range(3), repeat=3):
            for sticker in self.blocks[x][y][z].faces.values():
                if sticker.normal == self.normal:
                    j = x + x_offset - 1
                    i = y + y_offset - 1
                    pair_number = colors.index(sticker.color) + 1
                    screen.attron(curses.color_pair(pair_number))
                    screen.addch(int(i), int(j), block)  # TODO: Convert to ints elsewhere
                    screen.attroff(curses.color_pair(pair_number))


def init_colors():
    """
    Modify and then initialize color pairs to match an actual Rubiks cube.
    """
    colors = {
        20: 'C41E3A',  # red
        21: '0051BA',  # green
        22: '009E60',  # blue
        23: 'FFD500',  # yellow
        24: 'FF5800',  # orange
    }
    old_colors = {}
    for key, value in colors.items():
        old_colors[key] = curses.color_content(key)
        logging.info('old color: {}'.format(old_colors))
        r = int(value[0:2], 16) / 255 * 1000
        g = int(value[2:4], 16) / 255 * 1000
        b = int(value[4:6], 16) / 255 * 1000
        curses.init_color(key, int(r), int(g), int(b))
        logging.info('new color: {}'.format(curses.color_content(key)))

    curses.init_pair(1, 20, -1)  # red
    curses.init_pair(2, 21, -1)  # green
    curses.init_pair(3, 22, -1)  # blue
    curses.init_pair(4, curses.COLOR_WHITE, -1)  # white
    curses.init_pair(5, 23, -1)  # yellow
    curses.init_pair(6, 24, -1)  # orange

    return old_colors


def reset_colors(old_colors):
    """
    Terminal colours are fubar unless we reset them!
    """
    for key, (r, g, b) in old_colors.items():
        logging.info('{}, {}'.format(key, (r, g, b)))
        curses.init_color(key, r, g, b)


def main_loop(screen):
    """
    Run the main game loop.
    """
    screen.box()  # Render window frame
    cube = Cube()  # new cube
    cube.render(screen)

    while True:
        c = screen.getch()
        if c == ord('x'):  # Rotate about x-axis
            cube.rotate('x')
        elif c == ord('y'):  # Rotate about y-axis
            cube.rotate('y')
        elif c == ord('z'):  # Rotate about z-axis
            cube.rotate('z')  # TODO: How does this work?
        elif c == ord('j'):
            cube.twist(TOP)
        elif c == ord('i'):
            cube.twist(MIDDLE)  # horizontal
        elif c == ord('k'):
            cube.twist(BOTTOM)
        elif c == ord('h'):
            cube.twist(LEFT)
        elif c == ord('m'):
            cube.twist(CENTER)  # vertical
        elif c == ord('l'):
            cube.twist(RIGHT)
        elif c == ord('q'):
            break  # Exit the while loop
        screen.box()
        cube.render(screen)
        screen.refresh()


def game():
    """
    """
    cube = Cube()  # new cube
    print(cube.normal)
    print(cube.view)
    cube.show()
    cube.rotate('x')
    print(cube.normal)
    print(cube.view)
    cube.show()


def main(screen):
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    curses.use_default_colors()
    curses.start_color()  # Start colour mode
    if not curses.has_colors():
        sys.exit('Terminal does not support colors!')
    else:
        old_colors = init_colors()

    curses.curs_set(0)  # Hide cursor
    # TODO: @rubiks_colors decorator. Coooool.
    main_loop(screen)

    if curses.has_colors():
        reset_colors(old_colors)


if __name__ == '__main__':

    logging.basicConfig(filename='log/clipycube.log', filemode='w', level=logging.DEBUG)

    if len(sys.argv) > 1 and sys.argv[1] == 'ui':
        curses.wrapper(main)
    else:
        game()

