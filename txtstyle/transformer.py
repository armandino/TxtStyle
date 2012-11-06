import re
from linestyleprocessor import LineStyleProcessor

_DEFAULT = "\033[m"
_FOREGROUND = '38'
_BACKGROUND = '48'

# http://tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html
def _create_style_map():
    def add_256_colors(style_map, color_type):
        for i in range(1, 256):
            key = str(i) if color_type is _FOREGROUND else "on-%i" % i
            style_map[key] = "\x1b[%s;5;%im" % (color_type, i)

    # named styles
    style_map = {
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
    
    # 256 numeric colors
    add_256_colors(style_map, _FOREGROUND)
    add_256_colors(style_map, _BACKGROUND)
    return style_map

_STYLES = _create_style_map()

class Style:

    def __init__(self, pattern, transform_keys, apply_to_whole_line=False):
        self.regex_obj = re.compile(pattern)
        # list of transformations to apply e.g. bold, white, on-blue
        self.transforms = []
        self.apply_to_whole_line = apply_to_whole_line

        if transform_keys:
            for key in transform_keys:
                if key in _STYLES:
                    self.transforms.append(_STYLES[key])
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
            styled_line.append(_DEFAULT)
            
        styled_line.append(line[start : end])
        styled_line.append(_DEFAULT)
        
