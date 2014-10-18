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
import praw

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
    bottom_line.addstr(0, 0, "Front page")

    top_line.refresh()
    bottom_line.refresh()

    r = praw.Reddit(user_agent="rettyt 0.0.1 (HackTX 2014)")
    frontpage = r.get_front_page(limit=int((lines - 2) / 2))
    pos = 0
    for entry in frontpage:
        hpos = 0
        remainder.addch(pos, hpos, curses.ACS_UARROW)
        hpos += 2
        ups = str(entry.ups)
        remainder.addstr(pos, hpos, ups)
        hpos += len(ups) + 1
        downs = str(entry.downs)
        remainder.addch(pos, hpos, curses.ACS_DARROW)
        hpos += 2
        remainder.addstr(pos, hpos, downs)
        hpos += len(downs) + 1
        remainder.addstr(pos, hpos, entry.title)

        remainder.addstr(pos + 1, 0, entry.url)
        pos += 2

    remainder.refresh()
    while True:
        key = stdscr.getkey()
        if key == "q" or key == "Q" or key == "^C":
            return
        remainder.refresh()

def main():
    curses.wrapper(curses_main)
