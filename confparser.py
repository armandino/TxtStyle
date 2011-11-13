
import os
import re

from transformer import Style

__DEFAULT_CONF_FILE__ = '~/.txts'
__STYLE_HEADER__ = re.compile('\[\s*Style\s*=\s*\"?(\w+)\"?\s*\]')
__STYLE_DEF__ = re.compile('(.*):.*[\'|"](.*)[\'|"]')

#
# Style definition examples:
#
# blue: "some pattern \d+"
# red: 'some \w+ with single quotes'
#
# TODO: validate conf - i.e. style keys
#

class ConfParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class ConfParser:

    def __init__(self, conf_file=None):
        if conf_file:
            self.conf = conf_file
        else:
            self.conf = os.path.expanduser(__DEFAULT_CONF_FILE__)

    def get_styles(self, style_name):
        style_defs = self.__get_style_defs(style_name)
        styles = []
        for style_def in style_defs:
            style = self.__parse_style(style_def)
            styles.append(style)
        return styles

    def __parse_style(self, style_def):
        match = re.match(__STYLE_DEF__, style_def)
        if match:
            transforms = match.group(1).strip()
            pattern = match.group(2).strip()
            return Style(pattern, transforms)
        
        raise ConfParserException("Invalid style definition: %s" % style_def)

    def __get_style_defs(self, style_name):
        lines = self.__get_conf_file_lines()
        style_defs = []
        parsing_style = False

        for line in lines:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            
            if self.__is_style_header(line, style_name):
                parsing_style = True
            elif parsing_style and self.__is_style_header(line):
                break # next style def
            elif parsing_style:
                style_defs.append(line)
            
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

