#!/usr/bin/env python

import curses
import sys


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
    curses.start_color()  # Start colour mode
    if not curses.has_colors():
        sys.exit('Terminal does not support colors!')
    screen.clear()
    main_loop(screen)
    screen.refresh()


if __name__ == '__main__':
    curses.wrapper(main)

