# -*- coding: utf-8 -*-

import unittest
from umazero import _utils as utils

class TestUtils(unittest.TestCase):

    def test_flatten(self):
        self.assertEqual(utils.flatten([[1, 2], [3, 4], [5, 6]]), [1, 2, 3, 4, 5, 6])


if __name__ == '__main__':
    unittest.main()
