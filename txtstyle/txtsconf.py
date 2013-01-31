# -*- coding: utf-8 -*-

DEFAULT_CONF = """
# Available styles keys:
#
# - bold, underline, hidden
# - grey, red, green, yellow, blue, magenta, cyan, white
# - on-grey, on-red, on-green, on-yellow, on-blue, on-magenta, on-cyan, on-white
#
# The order of definitions matters, with highest precedence at the top.
#
# If a stlye definition starts with '!' then the whole line will be styled
# if it matches the given regex, and not just the match itself.

[Style="example"]
# Print in red any line containing the word 'error'
!red: regex("error")
red: regex("evil\.org")
# Date
green: regex("\d{4}-\d\d-\d\d")
# Time
green bold: regex("\d\d:\d\d:\d\d")
# IP address (and port number if present)
yellow underline: regex("\d+\.\d+\.\d+\.\d+(:\d+)?")
magenta: regex("\[samplesession\]")
# Catch-all for anything else inside [square brackets]
blue: regex("\[[^\]]+\]")
# Catch-all for any remaining standalone numbers
cyan bold: regex("\b\d+\b")

[Style="ifconfig"]
yellow bold: regex("\d+\.\d+\.\d+\.\d+(:\d+)?")
green bold: regex("(eth|wlan|lo)\d?")
blue bold: regex("(\d\d:?){6}")
red: regex("errors:\d+")
magenta: regex("[a-zA-Z]+:\d+")
cyan bold: regex("RX|TX|Link|inet\d?")

[Style="calendar"]
bold: regex("\d{4}")
172 bold underline: regex("Jan\w+|Feb\w+|Mar\w+|Apr\w+|May|Jun\w|Jul\w|Aug\w+|Sep\w+|Oct\w+|Nov\w+|Dec\w+")
229: regex("\d\d?")
160 bold: regex("Su")
220 bold: regex("\w+")

[Style="java"]
!red: regex("Exception")
white on-129 bold: regex("INFO|DEBUG|WARN")
green bold: regex("\(\w+\.java:\d+\)")
grey : regex("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d(,\d\d\d)?")
yellow: regex("[a-zA-Z]+:\d+")
yellow: regex("com\.[\w+|\.]+")
cyan: regex("org\.[\w+|\.]+")
blue: regex("\[[^\]]+\]")

[Style="ps"]
!white bold on-19: regex("USER       PID")
118: index(0-9)
160 bold: index(9-14)
215: index(15-19)
115: index(20-25)
162: index(25-32)
118: index(32-37)
207: index(38-46)
225: index(47-51)
45 bold: index(52-57)
120: index(59-64)
125: index(64-)

"""
