"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, 2013, 2014, 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

ONE_CHAR_REGEX = ['0', '1', '2', 'e']
STAR_OPERATOR = ['*']
BINARY_OPERATOR = ['.', '|']

def is_regex(s):

    if len(s) == 1 :
        res = s in ONE_CHAR_REGEX
    
    elif (len(s) >= 2) and (s[-1] in STAR_OPERATOR) :
        res = is_regex(s[:-1])
        
    elif (len(s) >= 5) and (s[0] == '(') and (s[-1] == ')') and even_para(s):
        new_s = s[1:-1]
        right_br_id = -1

        while new_s[-1] in STAR_OPERATOR:
            right_br_id -= 1

        if (new_s[0] == '(') :
            left, right, op = splice_from_left_operand(new_s)
            if op not in BINARY_OPERATOR:
                res = False
            else:
                res = is_regex(left) and is_regex(right)

        elif new_s[right_br_id] == ')' :
            left, right, op = splice_from_right_operand(new_s, right_br_id)
            if op not in BINARY_OPERATOR:
                res = False
            else:
                res = is_regex(left) and is_regex(right)
            
        else:
            for operator in BINARY_OPERATOR:
                if operator in new_s :
                    left, op, right = new_s.partition(operator)
            
            res = is_regex(left) and is_regex(right)
                
    else:
        res = False

    return res


def even_para(s):
    left_para = 0
    right_para = 0
    for char in s:
        if char == '(':
            left_para += 1
        if char == ')':
            right_para += 1
    return left_para == right_para


def splice_from_left_operand(s):
    br_counter = 1
    i = 0
    while br_counter != 0 :
        i += 1
        if s[i] == '(' :
            br_counter += 1
        if s[i] == ')' :
            br_counter -= 1
    
    while s[(i + 1)] in STAR_OPERATOR:
        i += 1

    op_index = i + 1
    
    left = s[:op_index]
    right = s[(op_index + 1):]
    op = s[op_index]

    return left, right, op


def splice_from_right_operand(s, right_br_id):
    br_counter = 1
    i = right_br_id
    while br_counter != 0 :
        i -= 1
        if s[i] == ')' :
            br_counter += 1
        if s[i] == '(' :
            br_counter -= 1

    op_index = i - 1
    
    left = s[:op_index]
    right = s[(op_index + 1):]
    op = s[op_index]
    
    return left, right, op


def build_regex_tree(regex):
    
    if len(regex) == 1:
        res = Leaf(regex)
    
    elif (len(s) >= 2) and (s[-1] in STAR_OPERATOR) :
        res = StarTree(build_regex_tree(s[:-1]))
        
    elif (len(s) >= 5) and (s[0] == '(') and (s[-1] == ')') and even_para(s):
        new_s = s[1:-1]

        while new_s[-1] in STAR_OPERATOR:
            new_s = new_s[:-1]

    return res