# emoji-picker-qtpy
PyQt5-🅱️ased emoji picker

## Why? 🤔

Because KDE Plasma's _Emoji Picker_ (`plasma.emojier`) neither goes to search textbox automatically nor allows user to navigate using arrow keys 🤦

## What it does? (features) 🤸

- alows to search emoji by name
- copies selected emoji to system clipboard
- immediately pastes selected emoji, assuming the picker was summoned with a text box focused
- closes on focus lost, `Esc` key pressed or emoji selected
- displayed emoji count is limited by how many of them fit inside the widget

For now it's possible to select emoji only using mouse pointer. Keyboard support coming soon!

## Dependencies 🧰

This project depends largery on [emoji_data_python](https://github.com/alexmick/emoji-data-python). This will likely get replaced by [emoji.json](https://github.com/github/gemoji/blob/master/db/emoji.json) since it contains more emoji and has more predictable names.

To install (almost) all dependencies run
```
pip install pyqt5 emoji_data_python Xlib pyautogui
```

Last dependency is the [Tkinter](https://docs.python.org/2/library/tkinter.html). 

Arch Linux users can install Tkinter by installing `tk` package from `extra` repository. While debian-based distro users should install `python3-tk` package.

## Serving suggestion 🥘

Create an executable shell script in an accessible location with following contents:
```
#!/bin/bash
python /(full path to directory containing the file)/emoji-picker-qt.py
```
and bind it to a keyboard shortcut (eg. using _Custom Shortcuts_ window in KDE Plasma).

## Planned features (in no particular order)

- arrow navigation (main priority)
- fuzzy search
- settings  (or just `.config` support)
- slack-style search (eg. searching for `:joy:` would give 😂)
- category tabs