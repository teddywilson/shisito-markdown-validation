#!/usr/bin/python
# -*- coding: UTF-8 -*-
# TODO fill this in with full unit tests

import unittest
import shisito

from shisito import ShisitoTestFailure
from shisito import ERROR_CODE_DEFAULT
from shisito import ERROR_CODE_NOT_FOUND
from shisito import ERROR_CODE_CORRUPTED_FILE
from shisito import ERROR_CODE_MISSING_FIELDS


class TestValidateConfig(unittest.TestCase):
    """shisito.validate_config() tests"""

    def test_configNotFoundThrowsException(self):
        try:
            shisito.validate_config('/tmp')
        except ShisitoTestFailure as e:
            self.assertEqual(e.code, ERROR_CODE_NOT_FOUND)
        except Exception:
            self.fail('unexpected exception raised')
        else:
            self.fail('ExpectedException not raised')

    def test_emptyConfigThrowsException(self):
        config = open('/tmp/shisito.yml', 'w')
        config.close()
        try:
            shisito.validate_config('/tmp/shisito.yml')
        except ShisitoTestFailure as e:
            self.assertEqual(e.code, ERROR_CODE_CORRUPTED_FILE)
        except Exception:
            self.fail('unexpected exception raised')
        else:
            self.fail('ExpectedException not raised')          

    """NOTE: config field validation will be covered by validate_document_has_allowlisted_keys() tests"""
    def test_validConfigSucceeds(self):
        config = open('/tmp/shisito.yml', 'w')
        config.write(""" collections:
                            -
                                filepattern: content/authors/*.md
                                fields:
                                - name: str
                            -
                                filepattern: content/books/*.md
                                fields:
                                - name: str
                                - author: str """)
        config.close()        
        try:
            shisito.validate_config('/tmp/shisito.yml')
        except Exception:
            self.fail('unexpected exception raised')
        else:
            pass
        

if __name__ == '__main__':
    unittest.main()