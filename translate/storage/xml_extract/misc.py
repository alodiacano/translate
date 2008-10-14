#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2002-2006 Zuza Software Foundation
# 
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with translate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from translate.misc.typecheck import accepts, Self, IsCallable, IsOneOf, Any

@accepts(IsCallable(), Any(), Any(), IsCallable(), vargs=[Any()])
def reduce_tree(f, parent_unit_node, unit_node, get_children, *state):
    """Enumerate a tree, applying f to in a pre-order fashion to each node.
    
    parent_unit_node contains the parent of unit_node. For the root of the tree,
    parent_unit_node == unit_node.
    
    get_children is a single argument function applied to a unit_node to
    get a list/iterator to its children.

    state is used by f to modify state information relating to whatever f does
    to the tree.
    """
    def as_tuple(x):
        if isinstance(x, tuple):
            return x
        else:
            return (x,)
    
    state = f(parent_unit_node, unit_node, *state)
    for child_unit_node in get_children(unit_node):
        state = reduce_tree(f, unit_node, child_unit_node, get_children, *as_tuple(state))
    return state

def compose_mappings(left, right):
    """Given two mappings left: A -> B and right: B -> C, create a
    hash result_map: A -> C. Only values in left (i.e. things from B)
    which have corresponding keys in right will have their keys mapped
    to values in right. """
    result_map = {}
    for left_key, left_val in left.iteritems():
        try:
            result_map[left_key] = right[left_val]
        except KeyError:
            pass
    return result_map