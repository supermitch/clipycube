#!/usr/bin/env python

import curses
import locale
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
        for row in range(6):
            row += x_offset
            for col in range(6):
                col += y_offset
                screen.addch(row, col, chr(0x2588))

def main_loop(screen):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    screen.box()

    cube = Cube()  # new cube

    while True:
        c = screen.getch()
        screen.clear()
        if c == ord('r'):
            cube.render(screen)
        elif c == ord('q'):
            break  # Exit the while loop
        else:
            screen.addch(12, 13, chr(0x2503))
        screen.refresh()


def main(screen):
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()
    curses.start_color()  # Start colour mode
    if not curses.has_colors():
        sys.exit('Terminal does not support colors!')
    screen.clear()
    main_loop(screen)


if __name__ == '__main__':
    curses.wrapper(main)

