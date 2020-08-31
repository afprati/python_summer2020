# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:47:42 2020

@author: miame
"""

import unittest
from day03_exercise_afp.py import *

class myTest(unittest.TestCase):
    
    def test_one(self):
        self.assertEqual(3, count_vowels("Reese"))
    
    def test_two(self):
        with self.assertRaises(TypeError):
            count_vowels(5)

if __name__ == '__main':
    unittest.main()