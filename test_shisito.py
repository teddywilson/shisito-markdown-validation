#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
import shisito

class Test(unittest.TestCase):
    def test_yep(self):
        shisito.main();
        

if __name__ == '__main__':
    unittest.main()