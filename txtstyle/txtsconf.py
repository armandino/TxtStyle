
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
#

[Style="example"]
# Print in red any line containing the word 'error'
!red: "error"
red: "evil\.org"
# Date
green: "\d{4}-\d\d-\d\d"
# Time
green bold: "\d\d:\d\d:\d\d"
# IP address (and port number if present)
yellow underline: "\d+\.\d+\.\d+\.\d+(:\d+)?"
magenta: "\[samplesession\]"
# Catch-all for anything else inside [square brackets]
blue: "\[[^\]]+\]"
# Catch-all for any remaining standalone numbers
cyan bold: "\b\d+\b"

[Style="ifconfig"]
yellow bold: "\d+\.\d+\.\d+\.\d+(:\d+)?"
green bold: "(eth|wlan|lo)\d?"
blue bold: "(\d\d:?){6}"
red: "errors:\d+"
magenta: "[a-zA-Z]+:\d+"
cyan bold: "RX|TX|Link|inet\d?"

[Style="calendar"]
bold: "\d{4}"
172 bold underline: "Jan\w+|Feb\w+|Mar\w+|Apr\w+|May|Jun\w|Jul\w|Aug\w+|Sep\w+|Oct\w+|Nov\w+|Dec\w+"
229: "\d\d?"
160 bold: "Su"
220 bold: "\w+"

[Style="syslog"]
!red bold: "<warn>"
on-magenta: "^\w\w\w \d\d\s?"
bold on-blue: "\d+:\d\d:\d+"
yellow: "\d+\.\d+\.\d+\.\d+"
red on-white: "\([^\)]+\)"
grey: "\[[^\]]+\]"

[Style="java"]
!red: "Exception"
#green: "INFO|DEBUG|WARN"
white on-129 bold: "INFO|DEBUG"
green bold: "\(\w+\.java:\d+\)"
grey : "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d(,\d\d\d)?"
yellow: "[a-zA-Z]+:\d+"
yellow: "com\.[\w+|\.]+"
cyan: "org\.[\w+|\.]+"
blue: "\[[^\]]+\]"

"""
