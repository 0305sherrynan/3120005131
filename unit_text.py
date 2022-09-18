import unittest
import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main.comparisonofsimilarity(['今天', '天气', '真', '挺好', '的'],
                                                     ['今天', '气候', '真', '挺不错', '的', ]), 0.6)  # add assertion here


if __name__ == '__main__':
    unittest.main()
