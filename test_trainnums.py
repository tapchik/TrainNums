import unittest
import custom_exceptions
import trainnums
import User

class test_trainnums(unittest.TestCase):

    def test_generate_task_all_settings_off(self):
        with self.assertRaises(custom_exceptions.UnableToGenerateProblemException):
            settings = User.Settings(False, False, False, False, 10, 10)
            task = trainnums.GenerateNewProblem(settings)

if __name__ == "__main__":
    unittest.main()