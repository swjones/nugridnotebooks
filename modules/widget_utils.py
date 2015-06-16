""" 
widget_utils.py

This module provides extra functions to aid in the production of interactive interfaces using the widget_framework.py module.
"""

import re
import keyword
import __builtin__

def float_text(string):
    for i in xrange(len(string)):
        if float_substring(string[:len(string)-i]):
            return string[:len(string)-i]
    return ""

def int_text(string):
    for i in xrange(len(string)):
        if int_substring(string[:len(string)-i]):
            return string[:len(string)-i]
    return ""

def token_text(string, strict=False):
    for i in xrange(len(string)):
        if token_substring(string[:len(string)-i], strict=strict):
            return string[:len(string)-i]
    return ""
    
def token_substring(string, strict=False):
    string=string.strip()
    if string == "":
        return False
    match = re.match("^[a-zA-Z_]\w*$", string)
    if strict and (keyword.iskeyword(string) or (string in dir(__builtin__))):
        return False
    if (match == None):
        return False
    else:
        return True

def float_substring(string):
    string=string.strip()
    if string == "":
        return True
    special_chars = ["+", "-", ".", "e", "E"]
    try:
        if string[-1] in special_chars:
            string = string + "0"
        float(string)
        return True
    except ValueError:
        return False

def int_substring(string):
    string=string.strip()
    if string == "":
        return True
    special_chars = ["+", "-"]
    try:
        if string[-1] in special_chars:
            string = string + "0"
        int(string)
        return True
    except ValueError:
        return False
