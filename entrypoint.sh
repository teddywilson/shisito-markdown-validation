#!/bin/bash
#
# Entrypoint for shisito.
# Args:
#   $1 = {TEST, RUN} execution mode

MODE_TEST=TEST
MODE_RUN=RUN

MODE=$1
if [[ ${MODE} == ${MODE_TEST} ]]
then
  python test_shisito.py
elif [[ ${MODE} == ${MODE_RUN} ]]
then
  python shisito.py
else
  echo "Unsupported mode ${MODE}"
  exit 1
fi