========
TxtStyle
========

TxtStyle is a command line tool for prettifying output of console
programs. It is primarily intended for simplifying the task of
visually scanning log files. This is done by highlighting text
using regular expressions.

Installation
============

$ tar xvf TxtStyle-x.y.z.tar.gz
$ cd TxtStyle-x.y.z
$ sudo python setup.py install


Usage
=====

  txts [file] [-n style] [-c configfile]

     file: Path to file to prettify

     n:    Style name
           If not specified text is printed unprocessed

     c:    Path to configuration file
           If not specified the default is ~/.txts.conf

Examples
--------

  # Apply style 'syslog' (defined in the default config file: ~/.txts.conf)
  txts /var/log/syslog -n syslog

  # Alternatively, file can be piped
  tail -f /var/log/syslog | txts -n syslog

  # Apply 'mystyle' defined in 'another.txts.conf'
  txts myapp.log -c /path/to/another.txts.conf -n mystyle


Source
======

$ git clone git://github.com/armandino/TxtStyle.git

