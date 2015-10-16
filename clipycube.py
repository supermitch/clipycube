#!/usr/bin/env python

import curses
import itertools
import locale
import logging
import operator
import random
import sys

import algebra


# Twist planes
MIDDLE = 'middle'
CENTER = 'center'
TOP = 'top'
BOTTOM = 'bottom'
LEFT = 'left'
RIGHT = 'right'


class Sticker(object):
    """ A block's sticker object. """
    def __init__(self, x, y, z, normal, color):
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
        """ Generate our Cube. """
        stickers = {}
        x = -1.5
        ys = range(-1, 2)
        zs = range(-1, 2)
        vector = (-1, 0, 0)  # left
        color = 'green'
        for y in ys:
            for z in zs:
                stickers[(x, y, z)] = Sticker(x, y, z, vector, color)

        x = 1.5
        ys = range(-1, 2)
        zs = range(-1, 2)
        vector = (1, 0, 0)  # right
        color = 'blue'
        for y in ys:
            for z in zs:
                stickers[(x, y, z)] = Sticker(x, y, z, vector, color)

        y = -1.5
        xs = range(-1, 2)
        zs = range(-1, 2)
        vector = (0, -1, 0)  # bottom
        color = 'red'
        for x in xs:
            for z in zs:
                stickers[(x, y, z)] = Sticker(x, y, z, vector, color)

        y = 1.5
        xs = range(-1, 2)
        zs = range(-1, 2)
        vector = (0, 1, 0)  # top
        color = 'orange'
        for x in xs:
            for z in zs:
                stickers[(x, y, z)] = Sticker(x, y, z, vector, color)

        z = -1.5
        xs = range(-1, 2)
        ys = range(-1, 2)
        vector = (0, 0, -1)  # back
        color = 'yellow'
        for x in xs:
            for y in ys:
                stickers[(x, y, z)] = Sticker(x, y, z, vector, color)

        z = 1.5
        xs = range(-1, 2)
        ys = range(-1, 2)
        vector = (0, 0, 1)  # front
        color = 'white'
        for x in xs:
            for y in ys:
                stickers[(x, y, z)] = Sticker(x, y, z, vector, color)

        return stickers

    def rotate(self, axis, sign=1):
        """ Reorient our cube by rotation about an axis. """
        # Reposition stickers
        for sticker in self.stickers.values():
            sticker.rotate(axis, sign=sign)

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
        for sticker in self.stickers.values():
            if comparison(sticker.coords[axis], 0):  # Only rotate stickers in the selected plane
                sticker.rotate(axis)

    def scramble(self):
        """ Scramble our faces. """
        planes = [TOP, MIDDLE, BOTTOM, RIGHT, CENTER, LEFT]
        for _ in range(3000):
            self.twist(random.choice(planes))

    def describe(self):
        """ Describe the cube's entire current layout. """
        print('Cube:')
        for sticker in self.stickers.values():
            print(sticker)
        print('\n')

    def show(self):
        """ Print the currently displayed face. """
        print('Front View:')
        for sticker in self.stickers.values():
            if sticker.is_visible(self.normal):
                print(sticker)
        print('\n')

    def render(self, screen):
        """ Render ourself. """
        colors = (None, 'red', 'green', 'blue', 'white', 'yellow', 'orange')

        height, width = screen.getmaxyx()
        x_offset, y_offset = int(width/2) - 1, int(height/2) - 1

        block_char = chr(0x2588)  # Python 3 only?
        for sticker in self.stickers.values():
            if sticker.is_visible(self.normal):
                x, y, z = sticker.coords
                j = x + x_offset
                i = y + y_offset
                pair_number = colors.index(sticker.color)
                screen.attron(curses.color_pair(pair_number))
                screen.addch(int(i), int(j), block_char)  # TODO: Convert to ints elsewhere
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
        logging.info('Old color: {} - {}'.format(key, old_colors))
        r = int(value[0:2], 16) / 255 * 1000
        g = int(value[2:4], 16) / 255 * 1000
        b = int(value[4:6], 16) / 255 * 1000
        curses.init_color(key, int(r), int(g), int(b))
        logging.info('New color: {} - {}'.format(key, curses.color_content(key)))

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
            cube.rotate(0)
        elif c == ord('y'):  # Rotate about y-axis
            cube.rotate(1)
        elif c == ord('z'):  # Rotate about z-axis
            cube.rotate(2)
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
        elif c == ord('s'):
            cube.scramble()
        elif c == ord('q'):
            break  # Exit the while loop
        screen.box()
        cube.render(screen)
        screen.refresh()


def game():
    """
    """
    cube = Cube()  # new cube
    cube.show()
    cube.rotate('x')
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
        old_colors = init_colors()

    curses.curs_set(0)  # Hide cursor
    # TODO: @rubiks_colors decorator. Coooool.
    main_loop(screen)

    if curses.has_colors():
        reset_colors(old_colors)


def main():
    logging.basicConfig(filename='log/clipycube.log', filemode='w', level=logging.DEBUG)

    if len(sys.argv) > 1 and sys.argv[1] == 'ui':
        curses.wrapper(curses_gui)
    else:
        game()


if __name__ == '__main__':
    main()

