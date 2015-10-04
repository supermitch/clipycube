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


def main_loop(screen):
    # screen.border(0)
    # screen.box(chr(0x0bf2), chr(0x0bf2))
    screen.addch(10, 10, chr(0x2501))
    screen.addch(10, 11, chr(0x2501))
    screen.addch(10, 12, chr(0x2501))
    screen.addch(10, 13, chr(0x2513))
    screen.addch(11, 13, chr(0x2503))
    screen.addch(12, 13, chr(0x2503))

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    screen.attron(curses.color_pair(1))
    screen.addstr(11, 10, chr(0x255F))
    screen.attroff(curses.color_pair(1))

    screen.addstr(12, 10, chr(0x255F))
    while True:
        c = screen.getch()
        if c == ord('p'):
            print('Printing document')
        elif c == ord('q'):
            break  # Exit the while loop
        elif c == curses.KEY_HOME:
            x = y = 0


def main(screen):
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()
    curses.start_color()  # Start colour mode
    if not curses.has_colors():
        sys.exit('Terminal does not support colors!')
    screen.clear()
    main_loop(screen)
    screen.refresh()


if __name__ == '__main__':
    curses.wrapper(main)

