# emoji-picker-qtpy
PyQt5-🅱️ased emoji picker

## Why? 🤔

Because KDE Plasma's _Emoji Picker_ (`plasma.emojier`) neither goes to search textbox automatically nor allows user to navigate using arrow keys 🤦

## What it does? (features) 🤸

- alows to search emoji by name
- emoji can be selected using keyboard arrows
- copies selected emoji to system clipboard
- immediately pastes selected emoji, assuming the picker was summoned with a text box focused
- closes on focus lost, `Esc` key pressed or emoji selected
- displayed emoji count is limited by how many of them fit inside the widget


## Dependencies 🧰

This project depends largery on [emoji_data_python](https://github.com/alexmick/emoji-data-python). This will likely get replaced by [emoji.json](https://github.com/github/gemoji/blob/master/db/emoji.json) since it contains more emoji and has more predictable names.

To install (almost) all dependencies run
```
pip install pyqt5 emoji_data_python Xlib pyautogui
```

Last dependency is the [Tkinter](https://docs.python.org/2/library/tkinter.html). 

Arch Linux users can install Tkinter by installing `tk` package from `extra` repository. While debian-based distro users should install `python3-tk` package.

This all works only if you have `python3` installed 👌

## Serving suggestion 🥘

Bind `emoji-picker-qt.py` to a keyboard shortcut as an executable script (eg. using _Custom Shortcuts_ in KDE Plasma). First line of the file takes care of running it with Python.

## Planned things (in no particular order)

- [ ] change emoji database to one with better (more natural) naming
- [ ] fuzzy search
- [ ] remove duplicated code
- [ ] settings  (or just `.config` support)
- [ ] slack-style search (eg. searching for `:joy:` would give 😂)
- [ ] category tabs
- [ ] get rid of global variables 
- [ ] clean up warparound conditions
- [x] ~~fix width for 2-character emojis~~ (fixed by installing `ttf-twemoji`)
- [x] ~~arrow navigation (main priority)~~ (done)