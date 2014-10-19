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
import praw

class Node(object):
    child = None
    sibling = None
    parent = None
    value = None

    def __init__(self, value, child=None, sibling=None, parent=None):
        self.value = value

def comments_to_tree(forest, parent=None):
    if len(forest) == 0:
        return None
    me = Node(forest[0], parent=parent)
    if hasattr(forest[0], 'body'):
        me.child = comments_to_tree(me.value.replies, me)
    me.sibling = comments_to_tree(forest[1:], parent)
    return me

def print_tree(node):
    if hasattr(node.value, 'body'):
        print(node.value.body)
        print()
    if node.child:
        print_tree(node.child)
    if node.sibling:
        print_tree(node.sibling)
