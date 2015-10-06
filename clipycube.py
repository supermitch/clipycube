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
        screen.addch(10, 10, chr(0x2501))
        screen.addch(10, 11, chr(0x2501))
        screen.addch(10, 12, chr(0x2501))
        screen.addch(10, 13, chr(0x2513))
        screen.addch(11, 13, chr(0x2503))
        screen.addch(12, 13, chr(0x2503))

        screen.attron(curses.color_pair(1))
        screen.addstr(11, 10, chr(0x255F))
        screen.attroff(curses.color_pair(1))

        screen.addstr(12, 10, chr(0x255F))


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

