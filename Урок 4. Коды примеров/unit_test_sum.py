import unittest

def test_sum_kv(i, j):
    return i * i + j * j

class TestSumKV(unittest.TestCase):

    def test_0equal(self):
        self.assertEqual(test_sum_kv(2, 3), 14)

    def test_1equal(self):
        self.assertEqual(test_sum_kv(2, 3), 13)





if __name__ == '__main__':
    unittest.main()
