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
    screen.addstr("Pretty text")

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    screen.attron(curses.color_pair(1))
    screen.addstr('\nVoila!!! In color...')
    screen.attroff(curses.color_pair(1))

    screen.addstr("\nMore Pretty text")
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

