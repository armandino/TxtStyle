#!/bin/bash

echo "Running argument tests..."

test_log="txtstyle/testdata/empty-log"

function assert_exit_code {
    expected=$1
    cmd="$2 &> /dev/null"
    eval $cmd
    actual=$?
    
    if [[ $expected -ne $actual ]]; then
        echo -e "\nExit code assertion error (expected, actual) = ($expected, $actual)"
        echo "For: $cmd"
    fi
}

# no args
assert_exit_code 0 "./txts"
# --name
assert_exit_code 0 "./txts --name java $test_log"
assert_exit_code 0 "./txts -n java $test_log"
# --regex
assert_exit_code 0 "./txts --regex 'some pattern' $test_log"
assert_exit_code 0 "./txts -r 'some pattern' $test_log"
assert_exit_code 0 "./txts --regex 'some pattern' --regex 'another pattern' $test_log"
assert_exit_code 0 "./txts -r 'some pattern' -r 'another pattern' $test_log"
assert_exit_code 0 "./txts $test_log --regex-rest 'some pattern' 'another pattern' 'yet another pattern'"
assert_exit_code 0 "./txts $test_log -R 'some pattern' 'another pattern' 'yet another pattern'"
# --conf
assert_exit_code 0 "./txts --conf txtstyle/testdata/test.txts.conf -n first $test_log"
assert_exit_code 0 "./txts -c txtstyle/testdata/test.txts.conf -n first $test_log"
# if --name is not specified then --conf is ignored
assert_exit_code 0 "./txts --conf INVALID_CONF_FILE"

# --color-always
assert_exit_code 0 "./txts --color-always $test_log"
assert_exit_code 0 "./txts --color-always -n java $test_log"
assert_exit_code 0 "./txts --color-always -r 'some pattern' $test_log"

# --version
assert_exit_code 0 "./txts --version"
assert_exit_code 2 "./txts -v"

#
# Verify errors
#
assert_exit_code 1 "./txts -n INVALID_STYLE_NAME $test_log"
assert_exit_code 2 "./txts INVALID_FILE_PATH"
assert_exit_code 2 "./txts --conf INVALID_CONF_FILE -n java"
# cannot combine --name and --regex
assert_exit_code 2 "./txts --name java --regex 'some pattern' $test_log"

echo "Done."
