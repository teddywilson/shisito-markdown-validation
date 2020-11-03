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


SHISITO_CONFIG_FILENAME = 'shisito.yml'


KEY_ROOT_DIR = 'root_dir'
KEY_CONFIG_PATH = 'config_path'
KEY_COLLECTIONS = 'collections'
KEY_SCHEMA = 'schema'
KEY_FILEPATTERN = 'filepattern'
KEY_FILENAME_REGEX = 'filename_regex'
KEY_REQUIRED = 'required'
KEY_VALUE = 'value'
KEY_UNIQUE = 'unique'
KEY_TYPE = 'type'
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


ERROR_CODE_DEFAULT=0
ERROR_CODE_NOT_FOUND=1
ERROR_CODE_CORRUPTED_FILE=2
ERROR_CODE_MISSING_FIELDS=3


class ShisitoTestFailure(Exception):
    """Exception raised when Shisito validation fails.

    Attributes:
        code -- Error Code
    """

    def __init__(self, message, code=ERROR_CODE_DEFAULT):
        self.code = code
        self.message = message
        super().__init__(self.message)


def __success(test_name):
  """Prints success result for a test name"""
  print('✅' + ' ' + test_name)


def __fail(error_message, code=ERROR_CODE_DEFAULT):
  """Fails test runner with a given error message"""
  raise ShisitoTestFailure('❌' + ' ' + error_message, code)


def __run_test(config, test):
  """Executes a test and prints out a success message if it passes"""
  test(config)
  __success(test.__name__)  


def __run_tests(config, tests):
  """Executes an array of tests"""
  for test in tests:
    __run_test(config, test)  


def __get_files(dir, filepattern):
  """Concatenates a directory and filepattern and returns all matching paths."""
  return [file for file in Path(dir).rglob(filepattern) if file.is_file()] 


def __validate_document_has_allowlisted_keys(doc, filepath, required_keys=[], optional_keys=[], required_values=[]):
  """Validates that a document contains all of the necessary keys and correct corresponding types"""
  required_keys_not_found = []
  invalid_types = []

  for key in required_keys:
    if key not in doc:
      required_keys_not_found.append(key)
    elif not isinstance(doc[key], required_keys[key]):
      __fail('Error parsing file: %s. Required key %s has invalid type %s which should be %s' % (
        filepath, key, type(doc[key]), required_keys[key]))
    if key in required_values and doc[key] != required_values[key]:
      __fail('Error parsing file: %s. Required key %s with required value `%s` equals `%s`' % (
        filepath, key, required_values[key], doc[key]))

  if required_keys_not_found:
    prefixed_required_keys_not_found = ["🔑 ~> " + key for key in required_keys_not_found] 
    __fail('Error parsing file: %s. Required keys not found:\n%s' % (
      filepath, "\n".join(prefixed_required_keys_not_found)))

  for key in optional_keys:
    if key not in doc:
      continue
    elif not isinstance(doc[key], optional_keys[key]):
      __fail('Error parsing file: %s. Optional key %s has invalid type %s which should be %s' % (
        filepath, key, type(doc[key]), optional_keys[key]))  
    if key in required_values and doc[key] != required_values[key]:
      __fail('Error parsing file: %s. Required key %s with required value `%s` equals `%s`' % (
        filepath, key, required_values[key], doc[key]))        


def __get_field_meta_or_fail(field, filepattern):
  field_name = next(iter(field))
  if not isinstance(field[field_name], list):
    __fail('Field `%s` metadata for filepattern %s must be in a list format' % (
      field_name, filepattern))
  field_meta = dict()
  for meta in field[field_name]:
    field_meta.update(meta)
  if KEY_TYPE not in field_meta:
    __fail('Field `%s` in filepattern %s must have a type' % (field_name, filepattern))
  # Validate the type is supported
  if field_meta[KEY_TYPE] not in SUPPORTED_TYPES:
    __fail('Type %s for field %s not currently supported.' % (field_meta[KEY_TYPE], field_name))
  # If a required value is present, ensure it matches the field's type
  if KEY_VALUE in field_meta and not isinstance(field_meta[KEY_VALUE], SUPPORTED_TYPES[field_meta[KEY_TYPE]]):
    __fail('Value %s for field %s does not match its required type of %s' % (
      field_meta[KEY_VALUE], field_name, field_meta[KEY_TYPE])) 
  return field_name, field_meta  


def __validate_config(root_dir):
  """Validates Shisito configuration file"""
  config_path = os.path.join(root_dir, SHISITO_CONFIG_FILENAME)
  if not os.path.isfile(config_path):
    __fail('%s not found!' % SHISITO_CONFIG_FILENAME, ERROR_CODE_NOT_FOUND)
  config = {}
  config[KEY_ROOT_DIR] = root_dir
  config[KEY_CONFIG_PATH] = config_path
  with open(config_path, 'r') as stream:
    docs = yaml.safe_load_all(stream)
    for doc in filter(None, docs):
      __validate_document_has_allowlisted_keys(doc, config_path, SHISITO_CONFIG_REQUIRED_KEYS);      
      for key in SHISITO_CONFIG_REQUIRED_KEYS:
        config[key] = doc[key]
      return config   
  __fail('Corrupted config file!', ERROR_CODE_CORRUPTED_FILE)


def __test_files_exist(config):
  """Validates that files exist for each defined collection."""
  for collection in config[KEY_COLLECTIONS]:
    filepattern = collection[KEY_FILEPATTERN]
    files = __get_files(config[KEY_ROOT_DIR], filepattern)
    _, counts = np.unique([file.parent for file in files ], return_counts=True)    
    if counts.sum() == 0:
      __fail('No files exist for filepattern: %s' % filepattern)
    else:
      __success('%d file(s) found at path: %s' % (counts.sum(), filepattern))


def __test_validate_types(config):
  """Validates fields and corresponding types for each collection."""
  for collection in config[KEY_COLLECTIONS]:
    filepattern = collection[KEY_FILEPATTERN]    
    fields = collection[KEY_SCHEMA]
    required_keys = {}
    required_values = {}
    optional_keys = {}
    # These will only ever be a 1-element dict
    for field in fields:
      field_name, field_meta = __get_field_meta_or_fail(field, filepattern)
      # Determine whether the field is required or not  
      if KEY_REQUIRED not in field_meta or field_meta[KEY_REQUIRED] is True:
        required_keys[field_name] = SUPPORTED_TYPES[field_meta[KEY_TYPE]]
      else:
        optional_keys[field_name] = SUPPORTED_TYPES[field_meta[KEY_TYPE]]
      if KEY_VALUE in field_meta:
        required_values[field_name] = field_meta[KEY_VALUE]
    files = __get_files(config[KEY_ROOT_DIR], filepattern)
    for file in files:
      with open(file, 'r') as stream:
        docs = yaml.safe_load_all(stream)
        for doc in filter(None, docs):
          __validate_document_has_allowlisted_keys(
            doc, file, required_keys, optional_keys, required_values)


def __test_filename_regex(config):
  """Validates that filenames in a collection match filename_regex if provided."""
  for collection in config[KEY_COLLECTIONS]:
    if KEY_FILENAME_REGEX in collection:
      filename_regex = collection[KEY_FILENAME_REGEX]
      filepattern = collection[KEY_FILEPATTERN]
      files = __get_files(config[KEY_ROOT_DIR], filepattern)
      for file in files:
        filename = os.path.basename(file)
        if not re.match(filename_regex, filename):
          __fail('%s does not match filename_regex: %s' % (file, filename_regex))


def __test_unique_fields(config):
  """Ensures that fields are unique across a collection, if uniqueness is specified."""
  for collection in config[KEY_COLLECTIONS]:
    filepattern = collection[KEY_FILEPATTERN]
    fields = collection[KEY_SCHEMA]
    unique_fields = set()
    visited_unique_fields = {}
    for field in fields:
      field_name, field_meta = __get_field_meta_or_fail(field, filepattern)
      if KEY_UNIQUE in field_meta and field_meta[KEY_UNIQUE] is True:
        unique_fields.add(field_name)
    files = __get_files(config[KEY_ROOT_DIR], filepattern)
    for file in files:
      with open(file, 'r') as stream:
        docs = yaml.safe_load_all(stream)
        for doc in filter(None, docs):
            for unique_field in unique_fields:
              if unique_field in doc and doc[unique_field] in visited_unique_fields:
                __fail('Unique field %s found in file %s already present in file %s' % (
                  unique_field, file, visited_unique_fields[doc[unique_field]]))
              visited_unique_fields[doc[unique_field]] = file


def run_shisito_tests(root_dir):
  """Main Shisito execution API"""
  print('🌶' +  ' ' + 'Running Shisito markdown valiation tests')

  try:
    config = __validate_config(root_dir)
    __run_tests(config, [
      __test_files_exist,
      __test_validate_types,
      __test_filename_regex,
      __test_unique_fields
    ])
  except ShisitoTestFailure as f:
    print(f.message)
    sys.exit(1)  

  print('😇 All tests pass!')
  sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
      raise Exception('Must provide project root directory as the first argument')
    print(sys.argv[0])
    run_shisito_tests(sys.argv[1])
