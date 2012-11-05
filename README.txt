========
TxtStyle
========

TxtStyle is a command line tool for prettifying output of console
programs. It is primarily intended for simplifying the task of
visually scanning log files. This is done by highlighting text
using regular expressions.

Installation
============

From source:

$ git clone git://github.com/armandino/TxtStyle.git
$ cd TxtStyle
$ sudo python setup.py install

From the archive:

$ tar xvf TxtStyle-x.y.z.tar.gz
$ cd TxtStyle-x.y.z
$ sudo python setup.py install


Usage
=====
TxtStyle [-n NAME | -r REGEX] [-c CONF] [--color-always] [filepath]

  filepath                 Path to a file.

  -n NAME, --name NAME     Name of the style to apply.
                           If not specified text is printed unprocessed

  -r REGEX, --regex REGEX  Highlight text based on the given regular expression.

  -c CONF, --conf CONF     Path to a conf file. Default is: ~/.txt.conf

  --color-always           Always use color. Similar to grep --color=always.


Examples
--------

  # Highlight given regex
  txts -r 'Foo|Bar' filename

  # Apply style 'syslog' (defined in the default config file: ~/.txts.conf)
  txts /var/log/syslog -n syslog

  # Alternatively, file can be piped
  tail -f /var/log/syslog | txts -n syslog

  # Apply 'mystyle' defined in 'another.txts.conf'
  txts myapp.log -c /path/to/another.txts.conf -n mystyle

  # Force color if output is piped to another script
  txts -n syslog /var/log/syslog --color-always | less -R
