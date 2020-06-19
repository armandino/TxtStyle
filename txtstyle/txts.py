# -*- coding: utf-8 -*-
#
# Copyright 2013-2020 Arman Sharif
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import errno
import itertools
import os
import sys
import time

from .confparser import ConfParser
from .confparser import ConfParserException
from .palette import Palette
from .transformer import Transformer
from .transformer import RegexStyle
from .txtsconf import *
from .version import VERSION

VERSION_INFO="""TxtStyle version %s.
Copyright (C) 2013 Arman Sharif.
Apache License v2.0 or later: <http://www.apache.org/licenses/LICENSE-2.0>
""" % VERSION

_USER_HOME_CONF_FILE = os.path.join(os.getenv('HOME'), '.txts.conf')

class Txts(object):

    def __init__(self, styles, filepath=None, color_always=False):
        self.transformer = Transformer(styles)
        self.filepath = filepath
        self.color_always = color_always

    def transform(self):
        if self.filepath:
            self._transform_file()
        elif not sys.stdin.isatty():
            self._transform_pipe()

    def _transform_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                for line in infile:
                    self._style(line)
        except KeyboardInterrupt:
            pass
        except IOError as e:
            if e.errno == errno.ENOENT:
                sys.stderr.write("File not found: %s\n" % self.filepath)
            elif e.errno == errno.EPIPE:
                # broken pipe
                pass
            else:
                sys.stderr.write("%s\n" % e)
            sys.exit(e.errno)

    def _transform_pipe(self):
        sys.stdin = sys.stdin.detach()

        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                self._style(line.decode('utf-8', errors='ignore'))
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdin.close()

    def _style(self, line):
        if sys.stdout.isatty() or self.color_always:
            styled_line = self.transformer.style(line.strip('\n'))
            sys.stdout.write(styled_line + '\n')
        else:
            sys.stdout.write(line)



def parse_args():
    parser = argparse.ArgumentParser(
        prog='TxtStyle',
        description='Prettifies output of console programs.')

    parser.add_argument('filepath', nargs='?', help='Path to a file.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--palette', help='Print a palette of available styles.', action='store_true')
    group.add_argument('-n', '--name', nargs=1, help='Name of the style to apply.')
    group.add_argument('-r', '--regex', nargs=1, action='append', help='Highlight text based on the given regular expression.')
    parser.add_argument('-c', '--conf', nargs=1, help='Path to a conf file. Default is: ~/.txt.conf')
    parser.add_argument('--color-always', help='Always use color. Similar to grep --color=always.', action='store_true')

    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument('--version', help='Print version information', action='store_true')
    return parser.parse_args()

def get_styles(conf_parser, style_def_name):
    try:
        return conf_parser.get_styles(style_def_name)
    except ConfParserException as e:
        sys.stderr.write("%s\n" % e)
        sys.exit(1)

def get_conf_lines(args):
    confpath = get_conf_path(args)
    with open(confpath, 'r') as f:
        return f.readlines()

def get_conf_path(args):
    if args.conf:
        # User-specified conf file
        filepath = args.conf[0]
        if not os.path.isfile(filepath):
            sys.stderr.write("File not found: %s\n" % filepath)
            sys.exit(errno.ENOENT)
        return filepath
    else:
        # User-home conf file (~/.txt.conf)
        if not os.path.isfile(_USER_HOME_CONF_FILE):
            with open(_USER_HOME_CONF_FILE, 'w+') as f:
                f.write(DEFAULT_CONF)
        return _USER_HOME_CONF_FILE

def loop_default_colors():
    while True:
        for style in ['bold','underline']:
            for col in ['red', 'green', 'blue', 'magenta', 'cyan', 'white']:
                yield ( col, style )

def main():
    args = parse_args()
    styles = []

    if args.version:
        sys.stdout.write(VERSION_INFO)
        sys.exit(0)
    elif args.palette:
        Palette().print_palette()
        sys.exit(0)
    elif args.name:
        conf_lines = get_conf_lines(args)
        conf_parser = ConfParser(conf_lines)
        style_def_name = args.name[0]
        styles = get_styles(conf_parser, style_def_name)
    elif args.regex:
        rexps = list(itertools.chain.from_iterable(args.regex))
        styles = [ RegexStyle(regex, style) for regex, style in zip(rexps, loop_default_colors()) ]

    txts = Txts(styles, args.filepath, args.color_always)
    txts.transform()

if __name__ == "__main__":
    main()

