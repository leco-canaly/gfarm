#!/bin/sh

source ./lib/funcs.sh

usage(){
    cat << EOS >&2
Usage:

    OPTION:
        -t TEST_NUMBER	Execute only TEST_NUMBER test
        -h		Help
EOS
exit 0
}

_ret=1
fail_flag=0
envdir="../../gfarm_environment"
expected_result_csv="expected-test-result.csv"
exec_test_num=0

## Opts. ##
while getopts t:h OPT; do
    case ${OPT} in
        t) exec_test_num=${OPTARG};;
        h) usage;;
        *) usage;;
    esac
done
shift `expr $OPTIND - 1`

if [ ! -f ${expected_result_csv} ]; then
    puts_error "not exist csv file."
    exit 1
fi

if [ ! -d ${envdir} ]; then
    puts_error "not exist gfarm_environment."
    exit 1
fi

if [ ${exec_test_num} -ne 0 \
    -a ${exec_test_num} -ne 1 \
    -a ${exec_test_num} -ne 2 \
    -a ${exec_test_num} -ne 4 \
    -a ${exec_test_num} -ne 5 \
    -a ${exec_test_num} -ne 7 \
    -a ${exec_test_num} -ne 8 \
    -a ${exec_test_num} -ne 9 \
    -a ${exec_test_num} -ne 10 ]; then
        puts_error "wrong argument."
        exit 1
fi

# test 1

# test 2

# test 4
if [ ${exec_test_num} -eq 0 -o ${exec_test_num} -eq 4 ]; then
    ./test4.sh
    if [ $? -ne 0 ]; then
        fail_flag=1
    fi
fi

# test 5

# test 7

# test 8

# test 9

# test 10

if [ ${fail_flag} -eq 0 ]; then
    _ret=0
fi

exit ${_ret}
