# clipycube

CLI based Rubiks Cube in Python.

## Requirements

Currently requires Python 3.x to run. This will change.

## Run

```shell
$ python3.4 clipycube ui
```

Running without `ui` argument causes it to run a test suite. This will change.

## Keyboard Shortcuts:

The entire program is operated via the keyboard.

### Program commands:

* `q` to Quit
* `3` to show 3<sup>rd</sup> angle projection
* `1` to return to front view

### Cube manipulation:

* `s` to Scramble the cube (via several thousand randomly selected twists)
* `S` to "Solve" the cube (resets it to solved state
* `x`, `y` or `z` to rotate in the clockwise direction about that axis
* `j`, `i` or `k` to twist the Bottom, Middle and Top faces, respectively
* `h`, `m` or `l` to twist the Left, Center and Right faces, respectively

Use capital letters, e.g. `X` or `J` to rotate or twist in opposite direction.

