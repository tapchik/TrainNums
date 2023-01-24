import numpy
import mysql.connector

DEBUG = True

class connector(object):
    db = None
    cursor = None
    def __init__(self):
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database = "trainnums")

        print("You are connected to...")
        print(self.db)

        # preparing a cursor object
        self.cursor = self.db.cursor()

    def insert(self):
        # TESTING INSERTING
        sql = "INSERT INTO table1 (user_id) VALUES (02)"
        #val = tuple("02")
        self.cursor.execute(sql)
        self.db.commit()

    def fetch_example_1(self):
        # TESTING SELECTING
        query = "SELECT * FROM table1"
        self.cursor.execute(query)

        myresult = self.cursor.fetchall()

        for x in myresult:
            print(x)

    def fetchProblem(self, user_id):
        query = f"select problem from table1 where user_id = {user_id}"
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        try:
            problem = myresult[0][0]
        except Exception:
            problem = None
        return problem

    def fetchAnswer(self, user_id):
        query = f"select answer from table1 where user_id = {user_id}"
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        try:
            answer = myresult[0][0]
        except Exception:
            answer = None
        return answer

    def addNewUser(self, user_id):
        sql = f"insert into table1 (user_id, state) values ({user_id, 0})"
        self.cursor.execute(sql)
        self.db.commit()

    def userExist(self, user_id):
        query = f"select user_id from table1 where user_id = {user_id}"
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        try:
            temp = myresult[0][0]
            return True
        except Exception:
            return False

    def updateUser(self, user):
        sql = f"update table1 set state = {user.state}, problem = {user.problem}, answer = {user.answer} where user_id = {user.user_id}"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            raise

    def close(self):
        self.db.close()

if DEBUG == True:
    c = connector()
    c.fetch_example_1()
    print(c.fetchProblem(1))
    print(c.fetchAnswer(1))
