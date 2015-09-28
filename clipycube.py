import curses
import sys


def main_loop(screen):
    screen.addstr("Pretty text")
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

