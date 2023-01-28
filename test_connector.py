import unittest
import custom_exceptions
import trainnums
import User
import connector
import sqlite3

class test_connector(unittest.TestCase):

    database: sqlite3.Connection

    def setUp(self) -> None:
        """
        Rollback database for testing to a starting point with no entries
        """
        self.database = sqlite3.connect("testing.db", check_same_thread=False)
        with open('RollbackDatabase.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        cursor = self.database.cursor()
        cursor.executescript(sql_script)
        self.database.commit()

    def test_generate_task_all_settings_off(self):
        pass

    def tearDown(self) -> None:
        """
        Closes database connection and quits testing connector module
        """
        self.database.close()

if __name__ == "__main__":
    unittest.main()