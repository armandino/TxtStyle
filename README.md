
# TxtStyle

TxtStyle is a command line tool for prettifying output of console
programs. It is primarily intended for simplifying the task of
visually scanning log files. This is done by highlighting text
using regular expressions.

## Installation

From source:

    git clone git://github.com/armandino/TxtStyle.git
    cd TxtStyle
    sudo python setup.py install

## Usage

To print help:

    txts -h

### Main options

To test the installation, run

    txts --name syslog /var/log/syslog

This should apply a style named 'syslog' to the log file.
Styles are defined in the conf file under user's home directory.

    ~/.txts.conf

### Usage examples

* Accept input from a pipe and apply a style
    $ tail -f /var/log/syslog | txts -n syslog

* Highlight Foo or Bar in the given file
    $ txts -r 'Foo|Bar' filename

* Apply 'mystyle' defined in 'another.txts.conf'
    $ txts myapp.log -c /path/to/another.txts.conf -n mystyle

* Force color if output is piped to another script
    $ txts -n syslog /var/log/syslog --color-always | less -R

