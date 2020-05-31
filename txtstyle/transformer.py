# -*- coding: utf-8 -*-

import re
from txtstyle.linestyleprocessor import LineStyleProcessor
from txtstyle.palette import DEFAULT_STYLE, NAMED_STYLE_MAP

_FOREGROUND = '38'
_BACKGROUND = '48'

# http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html
def _create_style_map():
    def add_numeric_styles(style_map, color_type):
        for i in range(1, 256):
            key = str(i) if color_type is _FOREGROUND else "on-%i" % i
            style_map[key] = "\x1b[%s;5;%im" % (color_type, i)

    style_map = NAMED_STYLE_MAP
    add_numeric_styles(style_map, _FOREGROUND)
    add_numeric_styles(style_map, _BACKGROUND)
    return style_map

_STYLES = _create_style_map()

class BaseStyle(object):

    def __init__(self, keys=[]):
        def error(key):
             raise Exception('Invalid style key: "%s"' % key)

        transforms = [(_STYLES[k] if k in _STYLES else error(k)) for k in keys]
        self.transforms = ''.join(transforms)

class RegexStyle(BaseStyle):
    def __init__(self, pattern, transform_keys, apply_to_whole_line=False):
        super(RegexStyle, self).__init__(transform_keys)
        self.regex_obj = re.compile(pattern)
        self.apply_to_whole_line = apply_to_whole_line

    def __repr__(self):
        return "RegexStyle[\"%s\", apply_to_whole_line = %s]" % \
            (self.regex_obj.pattern, self.apply_to_whole_line)


class IndexStyle(BaseStyle):
    """ Takes a list of indexes i.e. (start,end) tuples and transform keys.
    """
    def __init__(self, regions, transform_keys):
        super(IndexStyle, self).__init__(transform_keys)
        self.regions = regions


class Transformer(object):

    def __init__(self, styles):
        self.styles = styles
        self.line_style_processor = LineStyleProcessor()

    def style(self, line):
        if not self.styles:
            return line

        style_map = self.line_style_processor.get_style_map(line, self.styles)
        regions = sorted(style_map.keys())
        
        pos = 0
        styled_line = []
        for region in regions:
            style = style_map[region]
            start, end = region[0], region[1]

            if pos < start:
                self._append_to(styled_line, line, pos, start)

            self._append_to(styled_line, line, start, end, style)
            pos = end

        if pos <= len(line) - 1:
            self._append_to(styled_line, line, pos, len(line))
        
        return ''.join(styled_line)

    def _append_to(self, styled_line, line, start, end, style=None):
        if style:
            styled_line.append(style.transforms)
            
        styled_line.append(line[start : end])
        styled_line.append(DEFAULT_STYLE)
        
