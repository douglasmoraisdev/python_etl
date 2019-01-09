import unittest

from . import context

import app


class LoaderTestCase(unittest.TestCase):

    def test_sum_correctly(self):
        """Tests if loader sums correctly"""

        self.assertEqual(app.loader_sum_def(3,4), 7)

    def test_not_sum_correctly(self):
        """Tests if loader sums correctly"""

        self.assertEqual(app.loader_sum_def(3,4), 17)        

if __name__ == '__main__':
    unittest.main()
