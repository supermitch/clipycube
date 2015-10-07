#!/usr/bin/env python

import curses
import locale
import random
import sys


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
        x_offset, y_offset = 10, 10
        for row in range(3):
            row += x_offset
            for col in range(3):
                col += y_offset
                screen.attron(curses.color_pair(random.randrange(1, 7)))
                screen.addch(row, col, chr(0x2588))
                screen.attroff(curses.color_pair(random.randrange(1, 7)))


def init_colors():
    """
    Modify and then initialize color pairs to match an actual Rubiks cube.
    """
    colors = {
        curses.COLOR_RED: 'C41E3A',
        curses.COLOR_BLUE: '0051BA',
        curses.COLOR_GREEN: '009E60',
        curses.COLOR_YELLOW: 'FFD500',
        curses.COLOR_CYAN: 'FF5800',  # Make orange
    }
    for key, value in colors.items():
        r = int(value[0:2], 16) / 255 * 1000
        g = int(value[2:4], 16) / 255 * 1000
        b = int(value[4:6], 16) / 255 * 1000
        curses.init_color(key, int(r), int(g), int(b))

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)


def main_loop(screen):


    screen.box()

    cube = Cube()  # new cube

    while True:
        c = screen.getch()
        screen.clear()
        if c == ord('r'):
            cube.render(screen)
        elif c == ord('q'):
            break  # Exit the while loop
        screen.refresh()


def main(screen):
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()

    curses.start_color()  # Start colour mode
    if not curses.has_colors():
        sys.exit('Terminal does not support colors!')
    else:
        init_colors()

    screen.clear()
    curses.curs_set(0)  # Hide cursor
    main_loop(screen)


if __name__ == '__main__':
    curses.wrapper(main)

