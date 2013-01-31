# -*- coding: utf-8 -*-
#
# http://linuxtidbits.wordpress.com/2008/08/13/output-color-on-bash-scripts-advanced/
# The ANSI sequence: {ESC}[{attr};{bg};{256colors};{fg}m

import sys

DEFAULT_STYLE = "\033[m"
NAMED_STYLE_MAP = {
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

_LINE_LENGTH = 47

class Palette(object):

    def print_palette(self):
        self._named_styles()
        self._number_based_styles()

    def _separator(self, sepchar='='):
        print(' ' + sepchar * _LINE_LENGTH)

    def _print_style(self, key):
        sys.stdout.write("%s%s%s" % (NAMED_STYLE_MAP[key], key, DEFAULT_STYLE))

    def _named_styles(self):
        self._separator()
        print "                %sNamed styles%s" % (NAMED_STYLE_MAP['bold'], DEFAULT_STYLE)
        self._separator()
        self._justify("bold", "underline")
        self._justify("grey", "red", "green", "yellow")
        self._justify("blue", "magenta", "cyan", "white")
        self._justify("on-grey", "on-red", "on-green", "on-yellow")
        self._justify("on-blue", "on-magenta", "on-cyan", "on-white")

    def _number_based_styles(self):
        print
        self._separator()
        print "               %sNumeric styles%s" % (NAMED_STYLE_MAP['bold'], DEFAULT_STYLE)
        self._separator()
        for i in range(1, 256):
            sys.stdout.write("\x1b[38;5;%im [%3i]" % (i, i))
            if i % 8 == 0:
                print
        print
        self._separator()

    def _justify(self, *words):
        wordcount = len(words)
        charcount = len(''.join(words))
        fillsize = _LINE_LENGTH - charcount
        spacing = fillsize / (wordcount - 1)
        spacing_rem = fillsize % (wordcount - 1)

        sys.stdout.write(' ') # padding
        for word in words:
            self._print_style(word)
            sys.stdout.write(' ' * spacing)
            if spacing_rem > 0:
                sys.stdout.write(' ')
                spacing_rem -= 1
        print

