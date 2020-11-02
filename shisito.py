#!/usr/bin/python
# -*- coding: UTF-8 -*-
import io
import numpy as np
import os
import os.path
import re
import sys
import yaml

from pathlib import Path


SHISITO_CONFIG_DIR = '/github/workspace'
SHISITO_CONFIG_FILENAME = 'shisito.yml'
SHISITO_CONFIG_PATH = os.path.join(SHISITO_CONFIG_DIR, SHISITO_CONFIG_FILENAME)


KEY_COLLECTIONS = 'collections'
KEY_FIELDS = 'fields'
KEY_FILEPATTERN = 'filepattern'
KEY_TYPE_STR = 'str'
KEY_TYPE_INT = 'int'
KEY_TYPE_LIST = 'list'


SHISITO_CONFIG_REQUIRED_KEYS = {
  KEY_COLLECTIONS: list,
}


COLLECTION_REQUIRED_KEYS = {
  KEY_FILEPATTERN: str,
}


SUPPORTED_TYPES = {
  KEY_TYPE_STR: str,
  KEY_TYPE_INT: int,
  KEY_TYPE_LIST : list,
}


def success(test_name):
  """Prints success result for a test name"""
  print('✅' + ' ' + test_name)


def fail(error_message):
  """Fails test runner with a given error message"""
  print('❌' + ' ' + error_message)
  sys.exit(1)


def run_test(config, test):
  """Executes a test and prints out a success message if it passes"""
  test(config)
  success(test.__name__)  


def run_tests(config, tests):
  """Executes an array of tests"""
  for test in tests:
    run_test(config, test)  


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
    fail("""Shisito config not found! A shisito.yml config must be defined in your project's root directory.""")
  with open(SHISITO_CONFIG_PATH, 'r') as stream:
    docs = yaml.safe_load_all(stream)
    for doc in filter(None, docs):
      validate_document_has_allowlisted_keys(doc, SHISITO_CONFIG_PATH, SHISITO_CONFIG_REQUIRED_KEYS);
      config = {}
      for key in SHISITO_CONFIG_REQUIRED_KEYS:
        config[key] = doc[key]
      return config   


def test_files_exist(config):
  """Validates that files exist for each defined collection."""
  for collection in config[KEY_COLLECTIONS]:
    filepattern = collection[KEY_FILEPATTERN]
    files = [file for file in Path(SHISITO_CONFIG_DIR).rglob(filepattern)] 
    _, counts = np.unique([file.parent for file in files ], return_counts=True)    
    if counts.sum() == 0:
      fail('Test files exist failed for path: %s' % filepattern)
    else:
      success('%d file(s) found at path: %s' % (counts.sum(), filepattern))


def test_validate_types(config):
  """Validates fields and corresponding types for each collection."""
  for collection in config[KEY_COLLECTIONS]:
    fields = collection[KEY_FIELDS]
    required_keys = {}
    # These will only ever be a 1-element dict
    for field in fields:
      field_key = next(iter(field))
      field_val = field[field_key]
      # Validate the type is supported
      if field_val not in SUPPORTED_TYPES:
        fail('Type %s for field %s not currently supported.' % (field_val, field_key))
      required_keys[field_key] = SUPPORTED_TYPES[field_val]
    files = [file for file in Path(SHISITO_CONFIG_DIR).rglob(collection[KEY_FILEPATTERN])] 
    for file in files:
      with open(file, 'r') as stream:
        docs = yaml.safe_load_all(stream)
        for doc in filter(None, docs):
          validate_document_has_allowlisted_keys(doc, file, required_keys);
          success('Validated fields and types for file: %s' % file)


def main():
  print('🌶' +  ' ' + 'Running Shisito markdown valiation tests')

  config = validate_shisito_config()
  run_tests(config, [
    test_files_exist,
    test_validate_types
  ])

  print('😇 All tests pass!')
  sys.exit(0)


if __name__ == "__main__":
    main()