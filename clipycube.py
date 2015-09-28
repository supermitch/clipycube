import curses


def init_curses():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return screen


def quit_curses(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    screen = init_curses()
    quit_curses(screen)


if __name__ == '__main__':
    main()

