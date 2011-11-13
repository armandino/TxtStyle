# http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html
__STYLES__ = {
    "bold" : "\033[1m",
    "underline" : "\033[4m",
    "hidden" : "\033[4m",
    "grey" : "\033[30m", 
    "red" : "\033[31m",
    "green" : "\033[32m",
    "yellow" : "\033[33m",
    "blue" : "\033[34m",
    "magenta" : "\033[35m",
    "cyan" : "\033[36m",
    "white" : "\033[37m",
    "on-grey" : "\033[40m", 
    "on-red" : "\033[41m",
    "on-green" : "\033[42m",
    "on-yellow" : "\033[43m",
    "on-blue" : "\033[44m",
    "on-magenta" : "\033[45m",
    "on-cyan" : "\033[46m",
    "on-white" : "\033[47m"
    }

__DEFAULT__ = "\033[m"

import re
from linestyleprocessor import LineStyleProcessor

class Style:

    def __init__(self, pattern, transforms):
        self.regex_obj = re.compile(pattern)
        self.transforms = transforms

class Transformer:

    def __init__(self, styles):
        self.styles = styles
        self.line_style_processor = LineStyleProcessor()

    def style(self, line):
        if not self.styles:
            return line

        elected_regions = self.line_style_processor.get_elected_regions(
            line, self.styles)
        return self.__transform(line, elected_regions)

    def __transform(self, line, region_map):
        styled_line = ''
        regions = region_map.keys()
        regions.sort()
        
        pos = 0
        for region in regions:
            style = region_map[region]

            r_start = region[0]
            r_end = region[1] + 1
            region_str = ''

            if pos < r_start:
                region_str += self.__apply(line, pos, r_start)
                region_str += self.__apply(line, r_start, r_end, style)
            else:
                region_str += self.__apply(line, r_start, r_end, style)

            styled_line += region_str
            pos = r_end

        if pos < len(line) - 1:
            styled_line += self.__apply(line, pos, len(line)-1)
        
        return styled_line

    def __apply(self, line, start, end, style=None):
        style_escape_seq = __DEFAULT__
        if style:
            style_escape_seq = __STYLES__[style.transforms]

        region = line[start : end]
        
        return style_escape_seq + region + __DEFAULT__
