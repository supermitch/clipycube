"""
The curses related rendering stuff.
"""
import curses
import logging

import algebra  # TODO: Major no-no. Move this to Cube.


class Renderer(object):

    def __init__(self, screen, encoding):
        self.screen = screen
        self.encoding = encoding
        self.view_normal = (0, 0, 1)  # + z-axis, outwards of screen

    def add_help_strings(self):
        """ Display keyboard shortcuts when F1 is pressed. """
        start, col = 3, 5
        strings = [
            ('F1', 'Show/hide help'),
            ('q', 'Quit'),
            ('1', 'Show single (front) view'),
            ('3', 'Show orthographic (3rd angle) projection view'),
            ('s', 'Scramble'),
            ('S', 'Solve (reset)'),
            ('', ''),
            ('x/X', 'Rotate about x-axis'),
            ('y/Y', 'Rotate about y-axis'),
            ('z/Z', 'Rotate about z-axis'),
            ('', ''),
            ('h/H', 'Twist left plane'),
            ('m/M', 'Twist center plane'),
            ('l/L', 'Twist right plane'),
            ('', ''),
            ('j/J', 'Twist bottom plane'),
            ('i/I', 'Twist middle plane'),
            ('k/K', 'Twist Top plane'),
        ]
        for row, string in enumerate(strings, start=start):
            if string:
                self.screen.addstr(row, col, string[0], curses.A_BOLD)
                self.screen.addstr(row, col + 4, string[1])

    def render(self, cube, projection='default'):
        """ Render ourself. """
        colors = (None, 'red', 'green', 'blue', 'white', 'yellow', 'orange')

        normals = [(0, 0, 1), (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1)]
        offsets = [(0, 0), (-4, 0), (4, 0), (0, -4), (0, 4), (8, 0)]

        height, width = self.screen.getmaxyx()
        x_offset, y_offset = int(width/2) - 1, int(height/2) - 1

        block_char = chr(0x2588)  # Python 3 only?

        if projection == 'default':
            normals = normals[:1]  # Only render the first normal

        for normal, offset in zip(normals, offsets):
            for sticker in cube.stickers:
                if sticker.is_visible(normal):
                    angle = algebra.angle_between_vectors(normal, self.view_normal)
                    perp = algebra.cross_product(normal, self.view_normal)

                    if perp != (0, 0, 0):
                        rotation_axis = perp.index(1) if 1 in perp else perp.index(-1)
                        sign = 1 if 1 in perp else -1
                        new_coords = algebra.rotation(sticker.coords, rotation_axis, theta=angle, sign=sign)
                        x, y, z = new_coords
                    else:
                        x, y, z = sticker.coords

                    i = int(x + x_offset + offset[0])
                    j = int(y + y_offset + offset[1])
                    pair_number = colors.index(sticker.color)
                    self.screen.attron(curses.color_pair(pair_number))
                    self.screen.addch(j, i, block_char)
                    self.screen.attroff(curses.color_pair(pair_number))


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

