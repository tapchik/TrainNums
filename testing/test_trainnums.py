import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import unittest
import generate
import custom_exceptions
from models import Settings, Task

class test_trainnums(unittest.TestCase):

    def test_able_to_generate_problem(self):
        settings = Settings(True, False, False, False, 30, 10)
        task = generate.newProblem(settings)
        self.assertIsNotNone(task)

    def test_generate_task_all_settings_off(self):
        """Expected result: Being unable to generate new problem raises an error"""
        with self.assertRaises(custom_exceptions.UnableToGenerateProblemException):
            settings = Settings(False, False, False, False, 10, 10)
            task = generate.newProblem(settings)

if __name__ == "__main__":
    unittest.main()