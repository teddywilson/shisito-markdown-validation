#!/usr/bin/python
# -*- coding: UTF-8 -*-
# TODO fill this in with unit tests

import unittest
import shisito


class TestBasicAssertion(unittest.TestCase):
    def test_basicAssertion(self):
        self.assertEquals(True, True);
        

if __name__ == '__main__':
    unittest.main()