import os
import re

import transformer

#
# Style definition examples:
#
# blue: "some pattern \d+"
# red: 'some \w+ with single quotes'
#
__STYLE_DEF__ = re.compile('(.*):.*[\'|"](.*)[\'|"]')
__STYLE_HEADER__ = re.compile('\[\s*Style\s*=\s*\"?(\w+)\"?\s*\]')

class ConfParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class ConfParser:

    def __init__(self, conf_file):
        self.conf = conf_file

    def get_styles(self, style_name):
        style_defs = self.__get_style_defs(style_name)
        styles = []
        for style_def in style_defs:
            style = self.__parse_style(style_def)
            styles.append(style)
        
        self.__validate_styles(styles)
        return styles

    def __validate_styles(self, styles):
        for style in styles:
            if style.transforms not in transformer.__STYLES__.keys():
                raise ConfParserException('Invalid style attribute: "%s"'
                                          % style.transforms)

    def __parse_style(self, style_def):
        match = re.match(__STYLE_DEF__, style_def)
        if match:
            transforms = match.group(1).strip()
            pattern = match.group(2).strip()
            return transformer.Style(pattern, transforms)
        
        raise ConfParserException("Invalid style definition: %s" % style_def)

    def __get_style_defs(self, style_name):
        lines = self.__get_conf_file_lines()
        style_defs = []
        found_style = False

        for line in lines:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            
            if self.__is_style_header(line, style_name):
                found_style = True
            elif found_style and self.__is_style_header(line):
                break # next style def
            elif found_style:
                style_defs.append(line)
        
        if not found_style:
            raise ConfParserException('Style "%s" is not defined' % style_name)

        return style_defs
        
    def __is_style_header(self, line, style_name=None):
        match = re.match(__STYLE_HEADER__, line)
        if match:
            if style_name is not None:
                return style_name == match.group(1)
            return True
        
        return False

    def __get_conf_file_lines(self):
        f = open(self.conf)
        lines = f.readlines()
        f.close()
        return lines
