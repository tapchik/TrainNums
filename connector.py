import sqlite3
from User import User
import trainnums

def ExecuteQuery(database: sqlite3.Connection, query: str) -> list | None:
    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def UserExists(database: sqlite3.Connection, user_id: str) -> bool:
    query = f"select userid from user where userid=\"{user_id}\""
    query_result = ExecuteQuery(database, query)
    if len(query_result) == 0:
        return False
    else:
        return True

def InitiateNewUser(database: sqlite3.Connection, user_id: str) -> None:
    query = f"insert into user (userid) values (\"{user_id}\")"
    ExecuteQuery(database, query)
    database.commit()
    user = LoadInfoAboutUser(database, user_id)
    settings = user.extract_settings()
    user.problem, user.answer = trainnums.GenerateNewProblem(settings)
    UpdateInfoAboutUser(database, user)
    database.commit()

def LoadInfoAboutUser(database: sqlite3.Connection, user_id: str) -> User:

    # create new entry in database it case we don't have a record on user
    if UserExists(database, user_id) == False:
        InitiateNewUser(database, user_id)
    
    query = f"select * from user where userid = \"{user_id}\""
    query_result = ExecuteQuery(database, query)
    row = query_result[0]

    user = User(row)
    return user

def UpdateInfoAboutUser(database: sqlite3.Connection, user: User) -> None:
    query = f"update user set " + \
            f"userid = \'{user.id}\', " + \
            f"state = {user.state}, " + \
            f"problem = \'{user.problem}\', " + \
            f"answer = \'{user.answer}\', " + \
            f"addition = \'{int(user.addition)}\', " + \
            f"subtraction = \'{int(user.subtraction)}\', " + \
            f"multiplication = \'{int(user.multiplication)}\', " + \
            f"division = \'{int(user.division)}\', " + \
            f"max_sum = \'{user.max_sum}\', " + \
            f"max_factor = \'{user.max_factor}\', " + \
            f"correct = {user.correct}, " + \
            f"incorrect = {user.incorrect}, " + \
            f"skipped = {user.skipped} " + \
            f"where userid = {user.id}"
    ExecuteQuery(database, query)
    database.commit()
