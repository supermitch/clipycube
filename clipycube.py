import curses


def main(screen):
    print('In main')
    screen.clear()
    screen.refresh()


if __name__ == '__main__':
    curses.wrapper(main)

