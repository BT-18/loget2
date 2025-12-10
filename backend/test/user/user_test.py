import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from src.repository.user_repo import UserRepo

class UserRepoTest(unittest.TestCase):
    def __init__(self, pool) -> None:
        self.repo = UserRepo(pool)
        
    def test(self):
        print(self.repo.get_user_by_email("test@est.com"))



