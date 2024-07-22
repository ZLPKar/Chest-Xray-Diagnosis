import unittest
from users.user_management import register_user, check_credentials

class TestUserManagement(unittest.TestCase):
    def test_register_user(self):
        # Ensure that registering a new user works
        result = register_user('testuser', 'testpass')
        self.assertTrue(result)

    def test_check_credentials(self):
        # Ensure that checking credentials works
        register_user('testuser', 'testpass')  
        result = check_credentials('testuser', 'testpass')
        self.assertTrue(result)

