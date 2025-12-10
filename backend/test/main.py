import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.extend([BASE_DIR, SRC_DIR])

import unittest
from src.util.connector import Pool
from user.user_test import UserRepoTest

pool = Pool()

class TestMain(unittest.TestCase):
    def user_test(self):
        UserRepoTest(pool).test()

if __name__ == '__main__':
    unittest.main()