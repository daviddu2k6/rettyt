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
import textwrap
import rettyt.user as user
from sys import argv

top_line = None
body = None
bottom_line = None
r = None
sub = None
page_num = 0
current_entry = 0
pages = None
page = []
error = False
CTRL_R = 18

def clear_error():
    global error
    if error:
        error = False
        draw_modeline()

def show_error(string):
    global error
    error = True
    bottom_line.clear()
    bottom_line.addstr(string)
    bottom_line.refresh()

def load_subreddit():
    global body, current_entry, page_num, pages, page, sub
    pages = grab_screenful(curses.LINES - 2, subreddit=sub)
    page = next(pages)
    unpaint_line(body, current_entry)
    draw_submissions(page)
    current_entry = 0
    page_num = 1
    draw_modeline()
    paint_line(body, current_entry)

def draw_modeline():
    bottom_line.clear()
    theSub = "/r/" + sub if sub != "Front page" else sub
    uname_str = " [" + r.user.name + "]" if r.is_logged_in() else ""
    bottom_line.addstr(0, 0, "{} ({})".format(theSub,page_num) + uname_str)
    bottom_line.refresh()

def submission_to_string(submission, limit):
    left = "↑ {} ".format(submission.score).ljust(7, ' ')
    vote_status = submission.likes
    if vote_status is False:
        left = '↓' + left[1:]
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
    return left, title, right

def draw_submission(post, pos):
    global body
    (lines, cols) = body.getmaxyx()
    post_str = ''.join(submission_to_string(post, cols - 1))
    body.addstr(pos, 0, post_str)
    if post.likes is True:
        body.chgat(pos, 0, 1, curses.A_BOLD)

def draw_submissions(posts):
    global body
    top_line.clear()
    top_line.addstr(0, 0, "Enter: Open URL j: Down  k: Up c: Comments r: Refresh q: Quit")
    top_line.refresh()
    pos = 0
    body.clear()
    for entry in posts:
        draw_submission(entry, pos)
        pos += 1
    body.refresh()

def paint_line(window, line):
    window.chgat(line, 0, curses.color_pair(2))
    window.refresh()

def unpaint_line(window, line):
    window.chgat(line, 0, 0)
    window.refresh()

def get_input(prompt):
    global bottom_line
    cols = curses.COLS
    lines = curses.LINES
    bottom_line.clear()
    bottom_line.addstr(prompt)
    editor = curses.newwin(1, cols - len(prompt), lines - 1, len(prompt))
    editor.bkgd(ord(' '), curses.color_pair(1))
    bottom_line.refresh()
    tb = curses.textpad.Textbox(editor)
    ret = tb.edit()
    return ret.strip()

def grab_screenful(lines, subreddit='Front page'):
    global r
    ret = []
    if subreddit == 'Front page':
        submissions = r.get_front_page(limit=None)
    else:
        foo = r.get_subreddit(subreddit)#.get_hot(limit=None)
        submissions = foo.get_hot(limit=None)
    for post in submissions:
        ret.append(post)
        if len(ret) >= lines:
            yield ret
            ret = []
    yield ret
    return

def handle_key_posts_mode(stdscr, key):
    global top_line, bottom_line, body, r, sub, page_num, current_entry, page, pages
    if key == (curses.KEY_UP) or key == ord('k'):
        if current_entry > 0:
            unpaint_line(body, current_entry)
            current_entry -= 1
            paint_line(body, current_entry)
    elif key == curses.KEY_DOWN or key == ord('j'):
        if current_entry < len(page) - 1:
            unpaint_line(body, current_entry)
            current_entry += 1
            paint_line(body, current_entry)
    elif key == ord(' ') and len(page) != 0:
        page = next(pages)
        page_num += 1
        current_entry = 0
        body.clear()
        draw_submissions(page)
        paint_line(body, 0)
        draw_modeline()
    elif key == ord('\n'):
        webbrowser.open_new_tab(page[current_entry].url)
    elif key == ord('c'):
        comments_main(stdscr)
    elif key == ord('r'):
        load_subreddit()
    elif key == CTRL_R:
        draw_modeline()
        draw_submissions(page)
        paint_line(body, current_entry)
    elif key == ord('g'):
        oldSub = sub
        sub = get_input("Go to (blank for front page) /r/")
        bottom_line.clear()

        if not sub:
            sub = "Front page"
            draw_modeline()
        else:
            try:
                load_subreddit()
            except praw.errors.RedirectException:
                show_error("Invalid subreddit: " + sub)
                sub = oldSub
    elif key == ord('U') or key == ord('D') or key == ord('C'):
        if not r.is_logged_in():
            show_error("Can't vote without being logged in")
        else:
            post = page[current_entry]
            post.clear_vote()
            method = {'U' : post.upvote,
                      'D' : post.downvote,
                      'C' : post.clear_vote}[chr(key)]
            method()

def curses_main(stdscr):
    global top_line, bottom_line, body, r, sub, page_num, current_entry, page, pages
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

    sub = 'Front page' #hold on to this for future improvements, e.g., custom default subreddit
    pages = grab_screenful(lines-2, sub)
    page = next(pages)
    page_num = 1
    current_entry = 0
    draw_modeline()
    draw_submissions(page)
    paint_line(body, 0)
    while True:
        key = stdscr.getch()
        clear_error()
        if key == ord('q') or key == ord('Q') or key == 3:
            return
        handle_key_posts_mode(stdscr, key)
        body.refresh()

def comment_lines(comments, cols):
    ret = []
    for cmt in comments:
        if hasattr(cmt, 'body'):
            for line in textwrap.wrap(cmt.body, width=cols):
                ret.append(line)
            ret.append("")
    return ret

def comments_main(stdscr):
    top_line.clear()
    top_line.addstr(0, 0, "SPC: Down  b: Up c: Comments in browser q: Quit")
    top_line.refresh()
    cols = curses.COLS
    lines = curses.LINES - 2
    post = page[current_entry]
    
    # Put post title in bottom bar
    (_, cols) = body.getmaxyx()
    trunc_title = post.title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    if len(trunc_title) > cols - 1:
        trunc_title = trunc_title[0:cols-4] + '...' #leaves a clean chunk of space
    bottom_line.clear()
    bottom_line.addstr(0, 0, trunc_title)
    bottom_line.refresh()
    body.clear()
    body.refresh()

    comments = comment_lines(post.comments, cols)
    comment_start = 0
    comment_win = curses.newpad(len(comments), cols)
    for pos, line in enumerate(comments):
        comment_win.addstr(pos, 0, line)
    comment_win.refresh(comment_start, 0, 1, 0, lines, cols)
    while True:
        key = stdscr.getch()
        clear_error()
        if key == ord('q') or key == ord('Q') or key == 3:
            break
        elif key == ord('c'):
            webbrowser.open_new_tab(post.permalink)
        elif key == ord(' '):
            if comment_start + lines < len(comments):
                comment_start += lines
                body.clear()
                body.refresh()
        elif key == ord('b'):
            if comment_start - lines >= 0:
                comment_start -= lines
        comment_win.refresh(comment_start, 0, 1, 0, lines, cols)
    key = CTRL_R 
    handle_key_posts_mode(stdscr, key)
    return

def main():
    global r
    r = praw.Reddit(user_agent="rettyt 0.0.2 (HackTX 2014)")
    if len(argv) < 2 or argv[1] != "anon":
        user.load_config()
        user.login(r)
    curses.wrapper(curses_main)
    r.http.close()
