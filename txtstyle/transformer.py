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

    def __init__(self, pattern, transform_keys):
        self.regex_obj = re.compile(pattern)
        # list of transformations to apply e.g. bold, white, on-blue
        self.transforms = []

        if transform_keys:
            for key in transform_keys:
                if key in __STYLES__:
                    self.transforms.append(__STYLES__[key])
                else:
                    raise Exception('Invalid style attribute: "%s"' % key)


class Transformer:

    def __init__(self, styles):
        self.styles = styles
        self.line_style_processor = LineStyleProcessor()

    def style(self, line):
        if not self.styles:
            return line

        region_map = self.line_style_processor.get_region_map(line, self.styles)
        regions = region_map.keys()
        regions.sort()
        
        pos = 0
        styled_line = []
        for region in regions:
            style = region_map[region]
            start, end = region[0], region[1] + 1

            if pos < start:
                self._append_to(styled_line, line, pos, start)
                self._append_to(styled_line, line, start, end, style)
            else:
                self._append_to(styled_line, line, start, end, style)

            pos = end

        if pos <= len(line) - 1:
            self._append_to(styled_line, line, pos, len(line))
        
        return ''.join(styled_line)

    def _append_to(self, styled_line, line, start, end, style=None):
        if style:
            styled_line.append(''.join(style.transforms))
        else:
            styled_line.append(__DEFAULT__)
            
        styled_line.append(line[start : end])
        styled_line.append(__DEFAULT__)
        
