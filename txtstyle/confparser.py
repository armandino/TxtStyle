# -*- coding: utf-8 -*-

import os
import re
from .transformer import IndexStyle
from .transformer import RegexStyle

_STYLE_HEADER = re.compile('^\[\s*Style\s*=\s*\"?(\w+)\"?\s*\]$')
_REGEX_STYLE_DEF = re.compile('^(!?)([\w|\s|-]+):\s*regex\([\'|"](.+)[\'|"]\)$')
_INDEX_STYLE_DEF = re.compile('^([\w|\s|-]+):\s*index\(\s*(.+)\s*\)$')


class ConfParser(object):

    def __init__(self, conf_lines):
        self.conf_lines = conf_lines

    def get_styles(self, style_name):
        style_defs = self._get_style_defs(style_name)
        return [self._parse_style(s) for s in style_defs]

    def _parse_style(self, style_def):
        match = re.match(_REGEX_STYLE_DEF, style_def)
        if match:
            return self._parse_regex_style(match)

        match = re.match(_INDEX_STYLE_DEF, style_def)
        if match:
            return self._parse_index_style(style_def, match)

        raise ConfParserException("Invalid style definition: %s" % style_def)

    def _parse_regex_style(self, match):
        apply_to_whole_line = match.group(1).strip() == '!'
        transforms = match.group(2).strip().split()
        pattern = match.group(3).strip()
        return RegexStyle(pattern, transforms, apply_to_whole_line)

    def _parse_index_style(self, style_def, match):
        transforms = match.group(1).strip().split()
        # regionlist example: "0-10, 20-25, 50-"
        regionlist = match.group(2).strip().split(',')
        regions = []
        for regionitem in regionlist:
            idx = regionitem.split('-')
            if 1 > len(idx) > 2:
                raise ConfParserException("Invalid style definition: %s" % style_def)
            start = int(idx[0].strip())
            end = int(idx[1].strip()) if idx[1] else None
            if end and start >= end: # TODO: validate through regex
                raise ConfParserException(
                    "Invalid style definition: %s (Start index [%r] >= end index [%r])"
                    % (style_def, start, end))
            region = (start, end)
            regions.append(region)

        if not regions:
            raise ConfParserException("Invalid style definition: %s" % style_def)

        return IndexStyle(regions, transforms)

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
        return match and (style_name is None or style_name == match.group(1))


class ConfParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
