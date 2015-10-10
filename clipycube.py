#!/usr/bin/env python

import curses
import datetime
import locale
import logging
import random
import sys


logging.basicConfig(filename='{}.log'.format(datetime.date.today()),
                    level=logging.DEBUG)


class Block(object):
    """ One of the 26 blocks that makes up a Rubik's cube. """
    def __init__(self):
        self.orientation = None
        self.faces = []


class Cube(object):
    """ A Rubik's cube object. """
    def __init__(self):
        self.generate()
        self.scramble()

    def generate(self):
        """ Generate a new unscrambled cube. """
        pass

    def scramble(self):
        """ Scramble our blocks. """
        pass

    def render(self, screen):
        """ Render ourself. """
        height, width = screen.getmaxyx()
        x_offset, y_offset = int(width/2), int(height/2)
        for row in range(3):
            row += y_offset - 1
            for col in range(3):
                col += x_offset - 1
                screen.attron(curses.color_pair(random.randrange(1, 7)))
                screen.addch(int(row), int(col), 65)
                screen.attroff(curses.color_pair(random.randrange(1, 7)))


def init_colors():
    """
    Modify and then initialize color pairs to match an actual Rubiks cube.
    """
    colors = {
        20: 'C41E3A',
        21: '0051BA',
        22: '009E60',
        23: 'FFD500',
        24: 'FF5800',  # Make orange
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

    curses.init_pair(1, 20, -1)
    curses.init_pair(2, 21, -1)
    curses.init_pair(3, 22, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    curses.init_pair(5, 23, -1)
    curses.init_pair(6, 24, -1)

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
        if c == ord('r'):  # Redraw
            screen.box()
            cube.render(screen)
            screen.refresh()
        elif c == ord('q'):
            break  # Exit the while loop


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
    curses.wrapper(main)

