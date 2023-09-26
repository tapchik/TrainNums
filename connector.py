import sqlite3
from models import User, Task, Settings, Stats
import trainnums
from custom_exceptions import *

def UpdateInfoAboutUser(database: sqlite3.Connection, user: User) -> None:
    query = f"update user set " + \
            f"userid = \'{user.id}\', " + \
            f"state = {user.state}, " + \
            f"problem = \'{user.task.problem}\', " + \
            f"answer = \'{user.task.answer}\', " + \
            f"addition = \'{int(user.settings.addition)}\', " + \
            f"subtraction = \'{int(user.settings.subtraction)}\', " + \
            f"multiplication = \'{int(user.settings.multiplication)}\', " + \
            f"division = \'{int(user.settings.division)}\', " + \
            f"max_sum = \'{user.settings.max_sum}\', " + \
            f"max_factor = \'{user.settings.max_factor}\', " + \
            f"correct = {user.stats.correct}, " + \
            f"incorrect = {user.stats.incorrect}, " + \
            f"skipped = {user.stats.skipped} " + \
            f"where userid = {user.id}"
    #_ExecuteAlteringQuery(database, query)

class Connector:

    _connection: sqlite3.Connection

    def __init__(self, database: sqlite3.Connection):
        self._connection = database

    def GetTask(self, user_id: str) -> Task: 
        if self._UserExists(user_id) == False:
            self._InitiateNewUser(user_id)
        query = f"select * from task where user_id=\'{user_id}\'"
        row = self._ExecuteSelectQuery(query)[0]
        task = Task(row[1], row[2])
        return task

    def GetSettings(self, user_id: str) -> Settings:
        if self._UserExists(user_id) == False:
            self._InitiateNewUser(user_id)
        query = f"select * from settings where user_id=\'{user_id}\'"
        row = self._ExecuteSelectQuery(query)[0]
        settings = Settings(bool(row[1]), bool(row[2]), bool(row[3]), bool(row[4]), int(row[5]), int(row[6]))
        return settings
    
    def GetStats(self, user_id: str) -> Stats:
        if self._UserExists(user_id) == False:
            self._InitiateNewUser(user_id)
        query = f"select * from statistics where user_id=\'{user_id}\'"
        row = self._ExecuteSelectQuery(query)[0]
        stats = Stats(row[1], row[2], row[3])
        return stats
    
    def Save(self, user_id: str, object: Task | Stats | Settings) -> None:
        query = ""
        if type(object) == Task:
            query = f"""update task set problem=\'{object.problem}\', 
                                        answer=\'{object.answer}\' 
                                        where user_id=\'{user_id}\'"""
        elif type(object) == Settings:
            query = f"""update settings set addition=\'{int(object.addition)}\', 
                                          subtraction=\'{int(object.subtraction)}\', 
                                          multiplication=\'{int(object.multiplication)}\', 
                                          division=\'{int(object.division)}\', 
                                          max_sum={object.max_sum},
                                          max_factor={object.max_factor} 
                                          where user_id={user_id}"""
        elif type(object) == Stats:
            query = f"""update statistics set correct={object.correct}, 
                                              incorrect={object.incorrect}, 
                                              skipped={object.skipped}
                                              where user_id={user_id}"""
        self._ExecuteAlteringQuery(query)
    
    def GenerateNextTask(self, user_id: str) -> Task:
        settings = self.GetSettings(user_id)
        task = trainnums.GenerateNewProblem(settings)
        self.Save(user_id, task)
        return task

    def _UserExists(self, user_id: str) -> bool:
        query = f"select id from users where id=\'{user_id}\'"
        rows = self._ExecuteSelectQuery(query)
        if len(rows) > 0:
            return True
        return False
    
    def _InitiateNewUser(self, user_id: str) -> None:
        query = f"insert into users (id) values (\'{user_id}\')"
        self._ExecuteAlteringQuery(query)
        query = f"insert into task (user_id) values (\'{user_id}\')"
        self._ExecuteAlteringQuery(query)
        query = f"insert into settings (user_id) values (\'{user_id}\')"
        self._ExecuteAlteringQuery(query)
        query = f"insert into statistics (user_id) values (\'{user_id}\')"
        self._ExecuteAlteringQuery(query)
    
    def AbleToGenerateNewProblem(self, user_id: str) -> bool:
        settings = self.GetSettings(user_id)
        if any([settings.addition, settings.subtraction, settings.multiplication, settings.division]):
            return True
        return False

    def _ExecuteSelectQuery(self, query: str) -> list:
        cursor = self._connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def _ExecuteAlteringQuery(self, query: str) -> None:
        cursor = self._connection.cursor()
        cursor.execute(query)
        self._connection.commit()