# rettyt
Rettyt is a command-line (ncurses) Reddit client written for HackTX 2014.

## Controls
- `r`: Reply to the current post/comment
- '^R': Redraw the screen
- `U`: Upvote
- `D`: Downvowe
- `C`: Clear vote

### Subreddit browsing mode
- `k` or up arrow: Move to previous post
- `j` or down arrow: Move to next post
- Space: next page
- `B`: previous page
- Enter: Open post in web browser
- `c`: View comments
- `R`: Refresh subreddit
- `S`: Subscribe
- `^U`: Unsubscribe
- `g`: Go to subreddit
- `q`: Quit

### Comments browsing mode
- `c`: Open comments in browser
- Space or Enter: Scroll comment or advance to next comment
- `b`: Scroll back a page in the comment
- `n`: Next comment
- `p`: Back to previous comment
- `N`: Next comment at same depth
- `P`: Previous comment at same depth
- `u`: Up to parent

## rettytrc
Your rettytrc (`$HOME/.config/rettytrc` (Well, `XDG_CONFIG/rettytrc`) or `~/.rettytrc`) is a set of key-value pairs that
controls the behavior of the program.

The syntax is `key = value`. Comments using `#` are allowed.

- `username` is your Reddit username
- `password` is your password
- `editor` (optional) is the editor you use to compose replies (Blank files abort replies)

If you don't provvide a username or password, or call `rettyt anon`, you will not be logged in.
