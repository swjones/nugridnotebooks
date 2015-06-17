""" 
widget_utils.py

This module provides extra functions and classes to aid in the
production of interactive interfaces using the widget_framework.py
module.
"""

import re
import keyword
import __builtin__

class auto_styles:
    def __init__(self):
        self._line_count = 0
        self._line_styles = ["-", "--", "-.", ":", "None", " ", ""]
        self._line_colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
        self._line_markers = ["." ,",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "X", "D", "d", "|", "_", "None", None, " ", ""]
    
    def set_line_styles(self, line_styles):
        self._line_styles = line_styles
    
    def set_line_colors(self, line_colors):
        self._line_color = line_colors
    
    def set_line_markers(self, line_markers):
        self._line_markers = line_markers
    
    def reset_line_count(self):
        self._line_count = 0
        
    def get_style(self):
        style = {}

        if len(self._line_styles) != 0:
            line_style = self._line_styles[self._line_count % len(self._line_styles)]
            style["shape"] = line_style

        if len(self._line_colors) != 0:
            line_color = self._line_colors[self._line_count % len(self._line_colors)]
            style["color"] = line_color

        if len(self._line_markers) != 0:
            line_marker = self._line_markers[self._line_count % len(self._line_markers)]
            style["marker"] = line_marker
            
        self._line_count += 1
        return style

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
