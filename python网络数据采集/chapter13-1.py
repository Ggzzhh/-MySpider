# -*- coding: utf-8 -*-
"""单元测试的基础"""
import unittest


class TestAddition(unittest.TestCase):
    def setUp(self):
        print("测试开始")

    def tearDown(self):
        print("测试结束")

    def test_twoPlusTwo(self):
        total = 2 + 2
        self.assertEqual(4, total)


if __name__ == "__main__":
    unittest.main()