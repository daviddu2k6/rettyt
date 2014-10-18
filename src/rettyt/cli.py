# Copyright (C) 2014 Krzysztof Drewniak, David Du, and Tom Lu
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
import curses.textpad
import praw
import webbrowser

top_line = None
body = None
bottom_line = None

def submission_to_string(submission, limit):
    left = "↑ {} ".format(submission.score).ljust(7, ' ')
    right = " ({}) [/r/{}]".format(submission.domain,
                                   submission.subreddit.display_name)
    rawTitle = submission.title
    rawTitle = rawTitle.replace("&amp;", "&")
    rawTitle = rawTitle.replace("&lt;", "<")
    rawTitle = rawTitle.replace("&gt;", ">")
    titlelen = min(len(rawTitle), limit - len(left) - len(right) - 3)
    title = rawTitle[0:titlelen]
    if len(title) < len(rawTitle):
        title += "..."
    return left + title + right

def draw_submissions(posts):
    global body
    (lines, cols) = body.getmaxyx()
    pos = 0
    for entry in posts:
        post_str = submission_to_string(entry, cols - 1)
        body.addstr(pos, 0, post_str)
        pos += 1
    body.refresh()

def paint_line(window, line):
    window.chgat(line, 0, curses.color_pair(2))
    window.refresh()

def unpaint_line(window, line):
    window.chgat(line, 0, 0)
    window.refresh()

def grab_screenful(reddit, lines, subreddit=None):
    r = reddit
    ret = []
    if not subreddit:
        submissions = r.get_front_page(limit=None)
    else:
        submissions = r.get_subreddit(subreddit).get_hot(limit=None)
    for post in submissions:
        ret.append(post)
        if len(ret) >= lines:
            yield ret
            ret = []
    yield ret
    return

def curses_main(stdscr):
    global top_line, bottom_line, body
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    stdscr.refresh()
    cols = curses.COLS
    lines = curses.LINES

    top_line = curses.newwin(1, cols, 0, 0)
    bottom_line = curses.newwin(1, cols, lines - 1, 0)
    body = curses.newwin(lines - 2, cols, 1, 0)

    top_line.bkgd(ord(' '), curses.color_pair(1))
    bottom_line.bkgd(ord(' '), curses.color_pair(1))
    top_line.addstr(0, 0, "Enter: Open URL  j: Down  k: Up  q: Quit")
    bottom_line.addstr(0, 0, "Front page (1)")

    top_line.refresh()
    bottom_line.refresh()

    r = praw.Reddit(user_agent="rettyt 0.0.1 (HackTX 2014)")
    frontpages = grab_screenful(r, lines-2)
    frontpage = next(frontpages)
    page_num = 1
    current_entry = 0
    draw_submissions(frontpage)
    paint_line(body, 0)
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q') or key == 3:
            return
        elif key == (curses.KEY_UP) or key == ord('k'):
            if current_entry > 0:
                unpaint_line(body, current_entry)
                current_entry -= 1
                paint_line(body, current_entry)
        elif key == curses.KEY_DOWN or key == ord('j'):
            if current_entry < len(frontpage) - 1:
                unpaint_line(body, current_entry)
                current_entry += 1
                paint_line(body, current_entry)
        elif key == ord(' ') and len(frontpage) != 0:
            frontpage = next(frontpages)
            page_num += 1
            current_entry = 0
            body.clear()
            draw_submissions(frontpage)
            paint_line(body, 0)
            bottom_line.clear()
            bottom_line.addstr("Front page ({})".format(page_num))
            bottom_line.refresh()
        elif key == ord('\n'):
            webbrowser.open_new_tab(frontpage[current_entry].url)
        elif key == ord('r'):
            body.clear()
            draw_submissions(frontpage)
            paint_line(body, current_entry)
        elif key == ord('g'):
            bottom_line.clear()
            prompt = "Go to (blank for frontpage) /r/"
            bottom_line.addstr(prompt)
            editor = curses.newwin(1, cols - len(prompt), lines - 1, len(prompt))
            editor.bkgd(ord(' '), curses.color_pair(1))
            bottom_line.refresh()
            tb = curses.textpad.Textbox(editor)
            sub = tb.edit()
            bottom_line.clear()
            bottom_line.addstr(sub if (len(sub) > 0) else "Front page ({})".format(page_num))
            bottom_line.refresh()
        body.refresh()

def main():
    curses.wrapper(curses_main)
