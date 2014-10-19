import shlex
import praw
import appdirs
import os.path

config_keys = {}

def load_config():
    global config_keys
    paths = [os.path.join(appdirs.user_config_dir("", ""), "rettyt"),
             os.path.join(appdirs.user_config_dir("", ""), "rettytrc"),
             os.path.expanduser("~/.rettytrc"),
             os.path.expanduser("~/rettytrc"),
             os.path.abspath("rettytrc")]
    for path in paths:
        if os.path.isfile(path):
            fle = open(path, 'r')
            parser = shlex.shlex(fle)
            while True:
                (key, sep, val) = map(lambda x: parser.get_token(), range(0, 3))
                if key == '' or val == '':
                    break
                config_keys[key] = val
            fle.close()

def login(reddit):
    if "username" in config_keys and "password" in config_keys:
        reddit.login(config_keys["username"], config_keys["password"])
        return config_keys["username"] if reddit.is_logged_in() else None
    else:
        return None
