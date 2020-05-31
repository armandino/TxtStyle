#!/bin/bash

echo "Running argument tests..."

test_data_dir="tests/testdata"
test_log="${test_data_dir}/empty-log"

function assert_exit_code {
    expected=$1
    cmd="python txts-runner.py $2 &> /dev/null"
    eval $cmd
    actual=$?
    
    if [[ $expected -ne $actual ]]; then
        echo -e "\nExit code assertion error (expected, actual) = ($expected, $actual)"
        echo "For: $cmd"
    fi
}

# no args
assert_exit_code 0 ""
# --name
assert_exit_code 0 "--name java $test_log"
assert_exit_code 0 "-n java $test_log"
# --regex
assert_exit_code 0 "--regex 'some pattern' $test_log"
assert_exit_code 0 "-r 'some pattern' $test_log"
assert_exit_code 0 "--regex 'some pattern' --regex 'another pattern' $test_log"
assert_exit_code 0 "-r 'some pattern' -r 'another pattern' $test_log"
# --conf
assert_exit_code 0 "--conf $test_data_dir/test.txts.conf -n first $test_log"
assert_exit_code 0 "-c $test_data_dir/test.txts.conf -n first $test_log"
# if --name is not specified then --conf is ignored
assert_exit_code 0 "--conf INVALID_CONF_FILE"

# --color-always
assert_exit_code 0 "--color-always $test_log"
assert_exit_code 0 "--color-always -n java $test_log"
assert_exit_code 0 "--color-always -r 'some pattern' $test_log"

# --version
assert_exit_code 0 "--version"
assert_exit_code 2 "-v"

#
# Verify errors
#
assert_exit_code 1 "-n INVALID_STYLE_NAME $test_log"
assert_exit_code 2 "INVALID_FILE_PATH"
assert_exit_code 2 "--conf INVALID_CONF_FILE -n java"
# cannot combine --name and --regex
assert_exit_code 2 "--name java --regex 'some pattern' $test_log"

echo "Done."
