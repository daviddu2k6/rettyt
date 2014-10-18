# Copyright (C) 2014 Krzysztof Drewniak et. al.
# This file is part of Rettyt.

# Rettyt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Rettyt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Rettyt.  If not, see <http://www.gnu.org/licenses/>.
import curses

def curses_main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    stdscr.refresh()
    cols = curses.COLS
    lines = curses.LINES

    top_line = curses.newwin(1, cols, 0, 0)
    bottom_line = curses.newwin(1, cols, lines - 1, 0)
    remainder = curses.newwin(lines - 2, cols, 1, 0)

    top_line.bkgd(ord(' '), curses.color_pair(1))
    bottom_line.bkgd(ord(' '), curses.color_pair(1))
    top_line.addstr(0, 0, "Press q to quit")
    bottom_line.addstr(0, 0, "Test output for modeline")
    remainder.addstr(2, 2, "Hello, world")

    remainder.refresh()
    top_line.refresh()
    bottom_line.refresh()

    pos = 3
    while True:
        key = stdscr.getkey()
        if key == "q" or key == "Q" or key == "^C":
            return
        else:
            remainder.addstr(pos, 0, "Pressed key: " + key)
            pos += 1
            remainder.refresh()

def main():
    curses.wrapper(curses_main)
