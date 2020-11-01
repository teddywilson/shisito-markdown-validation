#!/usr/bin/python
# -*- coding: UTF-8 -*-
import io
import numpy as np
import os
import re
import sys
import yaml

from pathlib import Path

# TODO
ROOT_DIR = os.environ.get('SHISITO_MARKDOWN_DIR')
if ROOT_DIR is None:
  print('ROOT_DIR not set')
  sys.exit(1)

ALLOWLISTED_KEYS_REQUIRED = {
  'title': str,
  'permalink': str,
  'name': str,
  'state': str,
  'city': str,
  'layout': str,
  'recipients': list,
  'body': str
}

ALLOWLISTED_KEYS_OPTIONAL = {
  'cc': list,
  'expiration_date': str,
  'organization': str,
  'redirection_from': list,
  'subject': str
}


def success(test_name):
  """Prints success result for a test name"""
  print('✅' + ' ' + test_name)


def fail(error_message):
  """Fails test runner with a given error message"""
  print('❌' + ' ' + error_message)
  sys.exit(1)


def run_test(test):
  """Executes a test and prints out a success message if it passes"""
  test()
  success(test.__name__)  


def run_tests(tests):
  """Executes an array of tests"""
  for test in tests:
    run_test(test)


def get_markdown_files():
  """Fetches all markdown files recursively in the ${ROOT_DIR}"""
  markdown_files = []
  for subdir, dirs, files in os.walk(ROOT_DIR):
    for file in files:
      if file.endswith('.md'):
        markdown_files.append(os.path.join(subdir, file))
  return markdown_files      


def test_files_exist():
  """Tests that at least one markdown file exists in ${ROOT_DIR}"""
  files = [file for file in Path(ROOT_DIR).rglob('*.md')] 
  _, counts = np.unique([file.parent for file in files ], return_counts=True)
  if counts.sum() == 0:
    fail('test received no files at at path %s' % ROOT_DIR)

def validate_document_has_allowlisted_keys(doc, filepath):
  """Validates that a document contains all of the necessary keys and correct corresponding types"""
  required_keys_not_found = []
  invalid_types = []

  for key in ALLOWLISTED_KEYS_REQUIRED:
    if key not in doc:
      required_keys_not_found.append(key)
    elif not isinstance(doc[key], ALLOWLISTED_KEYS_REQUIRED[key]):
      fail('in file %s required key %s has invalid type %s should be %s' % (
        filepath, key, type(doc[key]), ALLOWLISTED_KEYS_REQUIRED[key]))
      
  if required_keys_not_found:
    prefixed_required_keys_not_found = ["🔑 ~> " + key for key in required_keys_not_found] 
    fail('in file %s required keys not found:\n%s' % (
      filepath, "\n".join(prefixed_required_keys_not_found)))

  for key in ALLOWLISTED_KEYS_OPTIONAL:
    if key not in doc:
      continue
    elif not isinstance(doc[key], ALLOWLISTED_KEYS_OPTIONAL[key]):
      fail('in file %s optional key %s has invalid type %s should be %s' % (
        filepath, key, type(doc[key]), ALLOWLISTED_KEYS_OPTIONAL[key]))


def test_files_contain_allowlisted_keys():
  """Tests that all markdown files contain required keys and corresponding types"""
  for filepath in get_markdown_files():
    with open(filepath, 'r') as stream:
      docs = yaml.safe_load_all(stream)
      for doc in filter(None, docs):
        validate_document_has_allowlisted_keys(doc, filepath)


def main():
  print('🔨 Running shisito tests...')

  run_tests([
    test_files_exist,
    test_files_contain_allowlisted_keys,
  ])

  print('😇 All tests pass!')
  sys.exit(0)

if __name__ == "__main__":
    main()