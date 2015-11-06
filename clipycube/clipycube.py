#!/usr/bin/env python

import curses
import itertools
import locale
import logging
import os
import sys

from cube import Cube
import renderer


def setup_logging():
    """ Set up log folder and configure logger. """
    root = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(root, 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename='log/clipycube.log', filemode='w', level=logging.DEBUG)


def main_loop(screen):
    """ Run the main game loop. """
    cube = Cube()
    the_renderer = renderer.Renderer(screen)

    projection = 'default'
    show_help = True
    while True:
        screen.erase()
        screen.box()
        the_renderer.render(cube, projection)
        if show_help:
            the_renderer.add_help_strings()
        if cube.solved:
            the_renderer.add_solved_string()
        screen.refresh()

        key = screen.getkey()
        logging.debug('Key press {}'.format(key))
        if key == 'KEY_F(1)':
            show_help = not show_help
        elif key == '1':
            projection = 'default'  # Front view
        elif key == '3':
            projection = 'multi'  # Orthographic projection view
        elif key == 'x':
            cube.rotate(0)  # Rotate about x-axis
        elif key == 'X':
            cube.rotate(0, sign=-1)  # Rotate about x-axis in CCW direction
        elif key == 'y':
            cube.rotate(1)
        elif key == 'Y':
            cube.rotate(1, sign=-1)
        elif key == 'z':
            cube.rotate(2)
        elif key == 'Z':
            cube.rotate(2, sign=-1)
        elif key == 'j':
            cube.twist('top')
        elif key == 'J':
            cube.twist('top', sign=-1)
        elif key == 'i':
            cube.twist('middle')  # horizontal
        elif key == 'I':
            cube.twist('middle', sign=-1)
        elif key == 'k':
            cube.twist('bottom')
        elif key == 'K':
            cube.twist('bottom', sign=-1)
        elif key == 'h':
            cube.twist('left')
        elif key == 'H':
            cube.twist('left', sign=-1)
        elif key == 'm':
            cube.twist('center')  # vertical
        elif key == 'M':
            cube.twist('center', sign=-1)
        elif key == 'l':
            cube.twist('right')
        elif key == 'L':
            cube.twist('right', sign=-1)
        elif key == 's':
            cube.scramble()
        elif key == 'S':
            cube.solve()
        elif key == 'q':
            break  # Exit the while loop
    screen.erase()  # Avoid flashing reset colours
    screen.refresh()


def curses_gui(screen):
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
    locale.setlocale(locale.LC_ALL, '')
    curses.wrapper(curses_gui)  # Wrapper will fix terminal on exceptions


if __name__ == '__main__':
    main()

