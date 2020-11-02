#!/bin/bash
#
# Entrypoint for shisito.
# Args:
#   $1 = If first arg is set to TEST, tests will be executed. Otherwise Shisito will execute normally.

MODE_TEST=TEST

MODE=$1
if [[ ${MODE} == ${MODE_TEST} ]]
then
  python test_shisito.py
else
  python shisito.py
fi
