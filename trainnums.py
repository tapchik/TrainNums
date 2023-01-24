import mysql.connector
from user import User


class TrainNums: 

    def __init__(self, host: str, user: str, password: str, base: str) -> None:
        self.database = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password, 
            database=base)
        self.cursor = self.database.cursor()

    
    def __getitem__(self, userid: int):
        # user = User(indices)
        return User(self._ExecuteQuery, userid)

    
    def _ExecuteQuery(self, query: str) -> list:
        cursorObject = self.database.cursor()
        cursorObject.execute(query)
        result = cursorObject.fetchall()
        return result
    
    def GetOne(self):
        query = "SELECT * from table1"
        myresult = self._ExecuteQuery(query)
        
        for x in myresult:
            print(x)
    
    def UserExists(self, userid: int) -> bool:
        query = f"select userid from table1 where userid={userid} limit 1"
        result = self._ExecuteQuery(query)
        if len(result) == 0:
            return False
        else:
            return True
    
    def _SetProblem(self, userid: int, problem: str, answer: str) -> bool: 
        query = f"update problem set problem=\'{problem}\', answer=\'{answer}\' where userid={userid}"
        self._ExecuteQuery()

