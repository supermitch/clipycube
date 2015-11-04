# -*- coding: UTF-8 -*-
import locale

def main(screen):
    code = locale.getpreferredencoding()
    while True:
        screen.erase()
        screen.box()
        screen.addch(10, 10, ord('a'))
        screen.addch(0x40007b)
        screen.addstr("Pretty text")
        screen.addstr('Ω')
        screen.addstr(20, 20, '█')

        # u = unichr(0x2588) + unichr(0x03A9)  # Block & Capital Omega
        # screen.addstr(code)
        # screen.addstr(u.encode(code))  # UnicodeEncodeError: 'ascii' codec can't encode u'\u2588'

        s = u"\u2588 \u03A9".encode(code)
        screen.addstr(s)

        screen.refresh()

        if screen.getkey() == 'q':
            break


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')

    print('Hello World')
    import curses
    curses.wrapper(main)
