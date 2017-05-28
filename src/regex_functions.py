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
    '''(str) -> bool
    
    Determine whether or not the inserted string is a valid regular expression
    or regex. Returns True if so, False if otherwise.
    
    >>> is_regex('1')
    True
    >>> is_regex('e')
    True
    >>> is_regex('123')
    False
    >>> is_regex('')
    False
    >>> is_regex('((1.2).(1.e*))')
    True
    >>> is_regex('((1.2).(1.e*)**)')
    True
    >>> is_regex('(1.(1|e*)*)')
    True
    >>> is_regex('((1|e*)*)')
    False
    '''
    # If the given string only has one char
    if len(s) == 1 :
        # Result is true if the one char is a valid regex single char
        res = s in ONE_CHAR_REGEX
    # If the string has a star operator at the end of it
    elif (len(s) >= 2) and (s[-1] in STAR_OPERATOR) :
        res = is_regex(s[:-1])
    # If the string has a binary operator within it
    elif (len(s) >= 5) and (s[0] == '(') and (s[-1] == ')') and even_para(s):
        # Get rid of the parantheses/brackets on the left/right most sides
        new_s = s[1:-1]
        star_counter = ''
        # Remove additional star operators to the right of the expression
        while new_s[-1] in STAR_OPERATOR:
            new_s = new_s[:-1]
            star_counter += '*'
        # Result is false if the original string contains several nested 
        # parantheses. For example, "((1.2))" .
        if check_nested_para(s):
            res = False
        # If the binary operator has another binary operator in the left
        # operand, or in both operands
        elif (new_s[0] == '(') :
            left, right, op = splice_from_left_operand(new_s)
            if op not in BINARY_OPERATOR:
                res = False
            else:
                res = is_regex(left) and is_regex(right + star_counter)
        # If the binary operator has another binary operator in only the
        # right operand
        elif new_s[-1] == ')' :
            left, right, op = splice_from_right_operand(new_s)
            if op not in BINARY_OPERATOR:
                res = False
            else:
                res = is_regex(left) and is_regex(right + star_counter)
        # If the binary operator has no binary operators in both operands
        else:
            # If the operator is a dot: "."
            if BINARY_OPERATOR[0] in new_s :
                left, op, right = new_s.partition('.')
                res = is_regex(left) and is_regex(right + star_counter)
            # If the operator is a bar: "|"
            elif BINARY_OPERATOR[1] in new_s :
                left, op, right = new_s.partition('|')
                res = is_regex(left) and is_regex(right + star_counter)
            # Result is false if the operator cannot be found
            else:
                res = False
    # Result is false if all other cases are exhausted/not applicable
    else:
        res = False

    return res


def even_para(s):
    '''(str) -> bool
        
    Determine whether or not the inserted string has an even number of
    parantheses/brackets. In other words, it finds out if all parantheses are
    appropriately closed/paired. This function aids in figuring out whether the
    inserted string is a valid regex.
    
    >>> even_para('()')
    True
    >>> even_para('(a(s)d)')
    True
    >>> even_para('(a(s)d))')
    False
    >>> even_para('((a(s)d))')
    True
    >>> even_para(')')
    False
    >>> even_para('')
    True
    '''
    # Keep track of how many left/right parantheses there are
    left_para = 0
    right_para = 0
    # Increment each counter up by one as it comes across parantheses
    for char in s:
        if char == '(':
            left_para += 1
        if char == ')':
            right_para += 1
    # Return whether there are the same number of left/right parantheses
    return left_para == right_para

def check_nested_para(s):
    '''(str) -> bool

    Return True iff the given string has a pair of parentheses within a pair
    of parantheses (nested brackets) immiediately next to each other. For
    example, '((abc))'. This function aids in determining whether
    the given string is a valid regular expression.
    
    REQ: Parantheses within the given string should be appropriately closed
    
    >>> check_nested_para('((1.2))')
    True
    >>> check_nested_para('((1.2).2)')
    False
    >>> check_nested_para('(1.(2|e*))')
    False
    >>> check_nested_para('((1.2).(2.e*)')
    False
    '''
    # Get rid of any * characters within the string
    s = s.replace('*', '')
    found_nested_left = True
    found_nested_right = True
    left_para_ids = [] 
    right_para_ids = []
    i = 0
    # Save the indexed locations of where the left/right brackets are found
    while i < len(s):
        if s[i] == '(':
            left_para_ids.append(i)
        if s[i] == ')':
            right_para_ids.append(i)
        i += 1
    # Nested brackets can only occur if there is more than one pair of
    # brackets within the string.
    if len(left_para_ids) > 1:
        # Find out whether each left bracket is right next to each other
        for i in range(1, len(left_para_ids)):
            check_id = (left_para_ids[i] - left_para_ids[i - 1]) != 1
            if check_id:
                found_nested_left = False
        # Find out whether each rightt bracket is right next to each other
        for i in range(1, len(right_para_ids)):
            check_id = (right_para_ids[i] - right_para_ids[i - 1]) != 1
            if check_id:
                found_nested_right = False    
        
        res = found_nested_left and found_nested_right
    # If more than one pair of parantheses is not found, nesting doesn't occur
    else:
        res = False
    
    return res

def splice_from_left_operand(s):
    '''(str) -> (set(str, str, str))
    Given a regular expression with a binary operator in the left operand
    or a binary operator in both left and right operands, return a set which
    breaks the string into the left operand, right operand and operator
    respectively.
    
    REQ: Given string should contain appropriately closed pairings of brackets
    
    >>> splice_from_left_operand('(1.2).e*')
    ('(1.2)', 'e*', '.')
    >>> splice_from_left_operand('(1.2).(e*.1)')
    ('(1.2)', '(e*.1)', '.')
    splice_from_left_operand('(1.0)*|(0|1)')
    >>> ('(1.0)*', '(0|1)', '|')
    '''
    # Find out where the left operand ends using the closed brackets
    br_counter = 1
    i = 0
    while br_counter != 0 :
        i += 1
        if s[i] == '(' :
            br_counter += 1
        if s[i] == ')' :
            br_counter -= 1
    # Sift through any additional '*'s that might be before the operator
    while ((i + 1) < len(s)) and s[(i + 1)] in STAR_OPERATOR:
        i += 1

    op_index = i + 1
    # Break up the string appropriately using the operator index
    left = s[:op_index]
    right = s[(op_index + 1):]
    op = s[op_index]

    return left, right, op


def splice_from_right_operand(s):
    '''(str) -> (set(str, str, str))
    Given a regular expression with a binary operator in the right operand,
    return a set which breaks the string into the left operand, right operand 
    and operator respectively.
    
    REQ: Given string should contain appropriately closed pairings of brackets
    REQ: Right operand cannot end in additional characters such as '*'
    
    >>> splice_from_right_operand('e|(1.0)')
    ('e', '(1.0)', '|')
    >>> splice_from_right_operand('2*|(1.0)')
    ('2*', '(1.0)', '|')
    >>> splice_from_right_operand('e*.(1.2)')
    ('e*', '(1.2)', '.')
    '''
    # Find out where the right operand ends starting from the right
    br_counter = 1
    i = len(s) - 1
    while br_counter != 0 :
        i -= 1
        if s[i] == ')' :
            br_counter += 1
        if s[i] == '(' :
            br_counter -= 1

    op_index = i - 1
    # Break up the string appropriately using the operator's index
    left = s[:op_index]
    right = s[(op_index + 1):]
    op = s[op_index]
    
    return left, right, op

def all_regex_permutations(s):
    '''(str) -> set of str
    Given a string, return all the permutations of that strings that are
    valid regular expressions.
    
    >>> all_regex_permutations('1')
    {'1'}
    >>> all_regex_permutations('4')
    set()
    >>> all_regex_permutations('e')
    {'e'}
    >>> all_regex_permutations('1*')
    {'1*'}
    >>> all_regex_permutations('*1')
    {'1*'}
    >>> all_regex_permutations('*101')
    set()
    >>> all_regex_permutations('(1.2)')
    {'(1.2)', '(2.1)'}
    >>> all_regex_permutations('(1.2*)')
    {'(1.2*)', '(2.1*)', '(1*.2)', '(2*.1)', '(1.2)*', '(2.1)*'}
    >>> len(all_regex_permutations('(2*.(2|1))'))
    60
    '''
    regex_perms = set()
    unique_perms = unique_permutations(s)
    # Return permutations of the given string, only if it is a valid regex
    for perm in unique_perms:
        if is_regex(perm):
            regex_perms.add(perm)
    
    return regex_perms

def unique_permutations(s):
    '''(str) -> set of str
    Given a string, return a set of all the unique permutations of that string
    without any repeated permutations of the same characters.
    
    >>> unique_permutations('aaa')
    {'aaa'}
    >>> unique_permutations('a')
    {'a'}
    >>> unique_permutations('aa')
    {'aa'}
    >>> unique_permutations('def')
    {'fde', 'fed', 'dfe', 'edf', 'efd', 'def'}
    '''
    unique_perms = set()
    all_perms = permutations(s)
    for perm in all_perms:
        unique_perms.add(perm)
    
    return unique_perms

def permutations(s, counter=0):
    '''(str) -> list of str
    Given a string, return a list of all possible permutations of that string.
    This includes repeated sequences when duplicate characters are involved.
    
    >>> permutations('aaa')
    ['aaa', 'aaa', 'aaa', 'aaa', 'aaa', 'aaa']
    >>> permutations('a')
    ['a']
    >>> permutations('aa')
    ['aa', 'aa']
    >>> permutations('def')
    ['def', 'dfe', 'edf', 'efd', 'fed', 'fde']
    '''
    
    if type(s) == str:
        s = list(s)
    
    if counter == len(s):
        word = ''
        for char in s:
            word += char
        res = [word]
    
    else:
        res = permutations(s, counter + 1)
        for i in range(counter + 1, len(s)):
            s[counter], s[i] = s[i], s[counter]
            res.extend(permutations(s, counter + 1))
            s[counter], s[i] = s[i], s[counter]

    return res
'''
def regex_match(r, s):
    if r.get_symbol() == 'e' and len(s) == 0 :
        res = True
    
    elif r.get_symbol() in ONE_CHAR_REGEX and len(s) == 1 :
        res = r.get_symbol() == s
    
    elif r.get_symbol() in STAR_OPERATOR :
        if r.get_children()[0].get_symbol() in s and r.get_children()[0].get_symbol() in ONE_CHAR_REGEX:
            not_match = False
            for i in range(len(s)):
                if s[i] != r.get_children()[0].get_symbol() :
                    not_match = True
            if not_match:
                res = False
            else:
                res = True
        #elif r.get_children()[0].get_symbol() in STAR_OPERATOR or r.get_children()[0].get_symbol() in BINARY_OPERATOR:
        else:
            res = regex_match(r.get_children()[0], s)
    elif r.get_symbol() in BINARY_OPERATOR:
        if r.get_symbol() == BINARY_OPERATOR[0]:
            if r.get_children[0].get_symbol() in ONE_CHAR_REGEX and r.get_children[1].get_symbol() in ONE_CHAR_REGEX :
                
    else:
        res = False
    
    return res
'''
def build_regex_tree(regex):
    '''(str) -> RegexTree
    Given a valid regular expression, produce and return a RegexTree object
    that represents regex.
    
    REQ: Given string must be a valid regular expression
    
    >>> build_regex_tree('1')
    Leaf('1')
    >>> build_regex_tree('(2|1)')
    BarTree(Leaf('2'), Leaf('1'))
    >>> build_regex_tree('((2|1).0*)')
    DotTree(BarTree(Leaf('2'), Leaf('1')), StarTree(Leaf('0')))
    >>> build_regex_tree('(2.(0.1)*)')
    DotTree(Leaf('2'), StarTree(DotTree(Leaf('0'), Leaf('1'))))
    '''
    # If the given valid regex is a single character, then it is a Leaf node
    if len(regex) == 1:
        res = Leaf(regex)
    # Start forming a StarTree if the last char in the regex is '*'
    elif (len(regex) >= 2) and (regex[-1] in STAR_OPERATOR) :
        res = StarTree(build_regex_tree(regex[:-1]))
    # Form a type of BinaryTree if the regex contains a binary expression
    elif (len(regex) >= 5) and (regex[0] == '(') and (regex[-1] == ')'):
        # Evaluate the insides of the brackets in the binary expression
        regex = regex[1:-1]
        star_counter = ''
        # Remove any * operators to the right of the binary expression to help
        # identify right binary operands properly; add them back on later
        while regex[-1] in STAR_OPERATOR:
            regex = regex[:-1]
            star_counter += '*'
        # If the left operand has a binary operator
        if (regex[0] == '(') :
            left, right, op = splice_from_left_operand(regex)
            # Form a DotTree or BarTree depending on the operator
            if op == BINARY_OPERATOR[0]:
                res = DotTree(build_regex_tree(left), build_regex_tree(
                    right + star_counter))
            else:
                res = BarTree(build_regex_tree(left), build_regex_tree(
                    right + star_counter))
        # If the right operand has a binary operator
        elif regex[-1] == ')' :
            left, right, op = splice_from_right_operand(regex)
            # Form a DotTree or BarTree depending on the operator
            if op == BINARY_OPERATOR[0]:
                res = DotTree(build_regex_tree(left), build_regex_tree(
                    right + star_counter))
            else:
                res = BarTree(build_regex_tree(left), build_regex_tree(
                    right + star_counter))
        # If neither operands have binary operators
        else:
            for operator in BINARY_OPERATOR:
                if operator in regex:
                    left, op, right = regex.partition(operator)
            # Form a DotTree or BarTree depending on the operator
            if op == BINARY_OPERATOR[0]:
                res = DotTree(build_regex_tree(left), build_regex_tree(
                    right + star_counter))
            else:
                res = BarTree(build_regex_tree(left), build_regex_tree(
                    right + star_counter))
    return res