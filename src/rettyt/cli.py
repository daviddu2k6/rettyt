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
import webbrowser

def draw_submissions(win, posts):
    cols = curses.COLS
    pos = 0
    for entry in posts:
        hpos = 0
        win.addstr(pos, hpos, "↑ ")
        hpos += 2
        ups = str(entry.ups)
        win.addstr(pos, hpos, ups)
        hpos += len(ups) + 1

        win.addnstr(pos, hpos, entry.title, cols - hpos)

        pos += 1
    win.refresh()

def paint_line(window, line):
    window.chgat(line, 0, curses.color_pair(2))
    window.refresh()

def unpaint_line(window, line):
    window.chgat(line, 0, 0)
    window.refresh()

def curses_main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    stdscr.refresh()
    cols = curses.COLS
    lines = curses.LINES

    top_line = curses.newwin(1, cols, 0, 0)
    bottom_line = curses.newwin(1, cols, lines - 1, 0)
    remainder = curses.newwin(lines - 2, cols, 1, 0)

    top_line.bkgd(ord(' '), curses.color_pair(1))
    bottom_line.bkgd(ord(' '), curses.color_pair(1))
    top_line.addstr(0, 0, "Enter: Open URL  j: Down  k: Up  q: Quit")
    bottom_line.addstr(0, 0, "Front page")

    top_line.refresh()
    bottom_line.refresh()

    r = praw.Reddit(user_agent="rettyt 0.0.1 (HackTX 2014)")
    frontpage = list(r.get_front_page(limit=lines - 2))
    current_entry = 0
    draw_submissions(remainder, frontpage)
    paint_line(remainder, 0)
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q') or key == 3:
            return
        elif key == (curses.KEY_UP) or key == ord('k'):
            if current_entry > 0:
                unpaint_line(remainder, current_entry)
                current_entry -= 1
                paint_line(remainder, current_entry)
        elif key == curses.KEY_DOWN or key == ord('j'):
            if current_entry < len(frontpage):
                unpaint_line(remainder, current_entry)
                current_entry += 1
                paint_line(remainder, current_entry)
        elif key == ord('\n'):
            webbrowser.open_new_tab(frontpage[current_entry].url)
        elif key == ord('r'):
            remainder.clear()
            draw_submissions(remainder, frontpage)
            paint_line(remainder, current_entry)
        remainder.refresh()

def main():
    curses.wrapper(curses_main)
