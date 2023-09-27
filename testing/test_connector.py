import unittest
import custom_exceptions
import generate
import connector
from connector import Connector
import sqlite3
import utils

class test_connector(unittest.TestCase):

    database: sqlite3.Connection
    connector: Connector
    user_id: str

    def setUp(self) -> None:
        """
        Rollback database for testing to a starting point with no entries
        """
        assets = utils.ReadAssetsFile('assets.yml')
        database_file: str = assets['DatabaseTesting']
        rollback_script_file: str = assets['RollbackScript']

        self.database = sqlite3.connect(database_file, check_same_thread=False)
        self.connector = Connector(self.database)
        self.user_id = '112233'

        with open(rollback_script_file, 'r') as sql_file:
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