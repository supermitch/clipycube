"""
The curses related rendering stuff.
"""
import curses
import logging

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

