# Clipycube

CLI based Rubiks Cube in Python.

## Requirements

Should run identically in both Python 2.x and 3.x!

## Run

```shell
$ python clipycube
```

## Keyboard Shortcuts:

The entire program is operated via the keyboard.

### Program commands:

* `F1` - show/hide help menu (keyboard shortcuts)
* `q` - Quit
* `3` - show 3<sup>rd</sup> angle projection
* `1` - return to front view

### Cube manipulation:

* `s` - scramble the cube (via several thousand randomly selected twists)
* `S` - "solve" the cube (just resets it to initial, solved state)
* `x`, `y` or `z` - rotate in the clockwise direction about that axis
* `j`, `i` or `k` - twist the Bottom, Middle and Top faces, respectively
* `h`, `m` or `l` - twist the Left, Center and Right faces, respectively

Use capital letters, e.g. `X`, `J`, to rotate or twist in the opposite directions.

