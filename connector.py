import sqlite3
from User import User
from User import Task
from User import Settings
from User import Stats
import trainnums
from custom_exceptions import *

def ExecuteSelectQuery(database: sqlite3.Connection, query: str) -> list:
    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def ExecuteAlteringQuery(database: sqlite3.Connection, query: str) -> None:
    cursor = database.cursor()
    cursor.execute(query)
    #result = cursor.fetchall()
    database.commit()
    #return result

def UserExists(database: sqlite3.Connection, user_id: str) -> bool:
    query = f"select userid from user where userid=\"{user_id}\""
    query_result = ExecuteSelectQuery(database, query)
    if len(query_result) == 0:
        return False
    else:
        return True

def InitiateNewUser(database: sqlite3.Connection, user_id: str) -> None:
    try:
        query = f"insert into user (userid) values (\"{user_id}\")"
        ExecuteAlteringQuery(database, query)
    except InitiatingUserThatAlreadyExistsException:
        return
    user = LoadInfoAboutUser(database, user_id)
    user.task = trainnums.GenerateNewProblem(user.settings)
    UpdateInfoAboutUser(database, user)

def LoadInfoAboutUser(database: sqlite3.Connection, user_id: str) -> User:

    # create new entry in database it case we don't have a record on user
    if UserExists(database, user_id) == False:
        InitiateNewUser(database, user_id)
    
    query = f"select * from user where userid = \"{user_id}\""
    query_result = ExecuteSelectQuery(database, query)
    row = query_result[0]

    task = Task(row[2], row[3])
    settings = Settings(bool(row[4]), bool(row[5]), bool(row[6]), bool(row[7]), int(row[8]), int(row[9]))
    stats = Stats(row[10], row[11], row[12])
    user = User(id=row[0], state=row[1], task=task, settings=settings, stats=stats)
    return user

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
    ExecuteAlteringQuery(database, query)
