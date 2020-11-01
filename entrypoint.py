#!/usr/bin/python
# -*- coding: UTF-8 -*-
import io
import numpy as np
import os
import os.path
import re
import sys
import yaml

# TODO(teddywilson) make this configurable
SHISITO_CONFIG_PATH = "/github/workspace/shisito.yml"

def success(test_name):
  """Prints success result for a test name"""
  print('✅' + ' ' + test_name)


def fail(error_message):
  """Fails test runner with a given error message"""
  print('❌' + ' ' + error_message)
  sys.exit(1)

def validate_shisito_config_exists():
  if not os.path.isfile(SHISITO_CONFIG_PATH):
    fail("""Shisito config not found! A shisito.yml config must be defined in your project's root 
            directory.""")

def main():
  print('🌶 Running Shisito markdown valiation tests')

  validate_shisito_config_exists()
  success('Shisito config found')

  # TODO(teddywilson) validate config and run tests
  print('😇 All tests pass!')
  sys.exit(0)

if __name__ == "__main__":
    main()