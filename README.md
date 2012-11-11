# TxtStyle

`TxtStyle` is a command line tool colorizing output of console programs.
It makes it easier to visually scan log files. Or it can be simply used
to make output prettier.

![TxtStyle](http://goo.gl/HcyUs)

## Try it out

    git clone git://github.com/armandino/TxtStyle.git
    cd TxtStyle

Apply 'example' style to example.log

    ./txts -n example example.log

Color ifconfig output

    ifconfig | ./txts -n ifconfig

Color calendar

    cal 2012 | ./txts -n calendar

Color ps output

    ps aux | txts -n ps

## Install

To install, execute the setup script in the `TxtsStyle` directory:

    sudo python2 setup.py install

(An alternative is to simply put the `txts` script on the `PATH`)

## Define your own styles

`TxtStyle` works by styling lines of text using regular expressions.
Styles are defined in the conf file under user's home directory:

    ~/.txts.conf

There are some example styles defined out of the box.
To define your own, add styles to the conf and reference them by name.

For example, add "mystyle"

    [Style="mystyle"]
    red: "foo"
    green bold: "bar"
    grey on-yellow: "baz"

and then apply the style using the `txts -n` (or `txts --name`) option:

    echo "My foo, bar, and baz." | txts -n mystyle

`TxtStyle` configuration supports a small set of **named** color keys
(such as `red`, `blue`, `yellow`) and an extended set of **numeric** keys
(from 1 to 255). To print available keys use the `-p` option:

    txts -p

## Other usage examples

Highlight text using the `-r` (or `--regex`) option. For example

    echo "A Foo and a Bar" | txts -r "Foo|Bar"

`TxtStyle` does not apply styles if output is piped to another command.
To force color if the output is piped, use `--color-always` option:

    ps aux | txts -n ps --color-always | less -R

Print basic help

    txts -h

