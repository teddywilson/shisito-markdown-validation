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

# TODO(teddywilson) build out more options
SHISITO_CONFIG_REQUIRED_KEYS = {
  'filepattern': str,
}

def success(test_name):
  """Prints success result for a test name"""
  print('✅' + ' ' + test_name)


def fail(error_message):
  """Fails test runner with a given error message"""
  print('❌' + ' ' + error_message)
  sys.exit(1)

def validate_document_has_allowlisted_keys(doc, filepath, required_keys=[], optional_keys=[]):
  """Validates that a document contains all of the necessary keys and correct corresponding types"""
  required_keys_not_found = []
  invalid_types = []

  for key in required_keys:
    if key not in doc:
      required_keys_not_found.append(key)
    elif not isinstance(doc[key], required_keys[key]):
      fail('Error parsing file: %s. Required key %s has invalid type %s which should be %s' % (
        filepath, key, type(doc[key]), required_keys[key]))
      
  if required_keys_not_found:
    prefixed_required_keys_not_found = ["🔑 ~> " + key for key in required_keys_not_found] 
    fail('Error parsing file: %s. Required keys not found:\n%s' % (
      filepath, "\n".join(prefixed_required_keys_not_found)))

  for key in optional_keys:
    if key not in doc:
      continue
    elif not isinstance(doc[key], optional_keys[key]):
      fail('Error parsing file: %s. Optional key %s has invalid type %s which should be %s' % (
        filepath, key, type(doc[key]), optional_keys[key]))  

def validate_shisito_config():
  """Validates Shisito configuration file"""
  if not os.path.isfile(SHISITO_CONFIG_PATH):
    fail("""Shisito config not found! A shisito.yml config must be defined in your project's root 
            directory.""")
  with open(SHISITO_CONFIG_PATH, 'r') as stream:
    docs = yaml.safe_load_all(stream)
    for doc in filter(None, docs):
      validate_document_has_allowlisted_keys(doc, SHISITO_CONFIG_PATH, SHISITO_CONFIG_REQUIRED_KEYS);  
      # TODO(teddywilson) return mapping of required keys and values          

def main():
  print('🌶 Running Shisito markdown valiation tests')

  print('🔎 Validating Shisito config')
  validate_shisito_config()
  success('Shisito config validated')

  # TODO(teddywilson) files exists test
  # TODO(teddywilson) field and type validation tests

  print('😇 All tests pass!')
  sys.exit(0)

if __name__ == "__main__":
    main()