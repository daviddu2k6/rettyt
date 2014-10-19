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
import praw.objects

class Node(object):
    child = None
    sibling = None
    parent = None
    value = None
    lsibling = None

    def __init__(self, value, child=None, sibling=None, parent=None):
        self.value = value

    def setSibling(self, node):
        self.sibling = node
        if node:
            node.lsibling = self

def comments_to_tree(forest, parent=None):
    if len(forest) == 0:
        return None
    me = Node(forest[0])
    me.parent = parent
    if not isinstance(me.value, praw.objects.MoreComments):
        me.child = comments_to_tree(me.value.replies, parent=me)
    me.setSibling(comments_to_tree(forest[1:], parent=parent))
    return me

def print_tree(node):
    if not isinstance(node.value, praw.objects.MoreComments):
        print(node.value.body)
        print()
    if node.child:
        print_tree(node.child)
    if node.sibling:
        print_tree(node.sibling)
