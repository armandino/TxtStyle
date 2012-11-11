import os
import re

import transformer

#
# Style definition examples:
#
# blue: "some pattern \d+"
# red: 'some \w+ with single quotes'
# !green on-yellow: "! applies style to the whole line"
_STYLE_DEF = re.compile('^(!?)([\w|\s|-]+):\s*[\'|"](.+)[\'|"]$')
_STYLE_HEADER = re.compile('^\[\s*Style\s*=\s*\"?(\w+)\"?\s*\]$')

class ConfParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class ConfParser(object):

    def __init__(self, conf_lines):
        self.conf_lines = conf_lines

    def get_styles(self, style_name):
        style_defs = self._get_style_defs(style_name)
        styles = []
        for style_def in style_defs:
            style = self._parse_style(style_def)
            styles.append(style)
        return styles

    def _parse_style(self, style_def):
        match = re.match(_STYLE_DEF, style_def)
        if match:
            apply_to_whole_line = match.group(1).strip() == '!'
            parsed_transforms = match.group(2).strip()
            pattern = match.group(3).strip()
            transforms = parsed_transforms.split()
            return transformer.Style(pattern, transforms, apply_to_whole_line)
        
        raise ConfParserException("Invalid style definition: %s" % style_def)

    def _get_style_defs(self, style_name):
        style_defs = []
        is_style_header = False

        for line in self.conf_lines:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            
            if self._is_style_header(line, style_name):
                is_style_header = True
            elif is_style_header and self._is_style_header(line):
                break # next style def
            elif is_style_header:
                style_defs.append(line)
        
        if not is_style_header:
            raise ConfParserException('Style "%s" is not defined' % style_name)

        return style_defs
        
    def _is_style_header(self, line, style_name=None):
        match = re.match(_STYLE_HEADER, line)
        if match:
            if style_name is not None:
                return style_name == match.group(1)
            return True
        
        return False
