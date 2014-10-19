import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "rettyt",
    version = "0.0.2",
    author = "Krzysztof Drewniak, David Du, and Tom Lu",
    author_email = "krzysdrewniak@gmail.com",
    description = "Command-line reddit client",
    license = "GPL",
    package_dir = {'': 'src'},
    packages = ["rettyt"],
    long_description = read("README"),
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    entry_points = {
        'console_scripts' : ['rettyt=rettyt.cli:main']
    }
)
