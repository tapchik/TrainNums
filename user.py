from random import choice, randint
from enum import Enum
from custom_exceptions import *

class User: 

    def __init__(self, database, userid: str):
        self.userid = str(userid)
        self.CursorObject = database.cursor()
        if self.Exists == False:
            self.Create()
            self.GenerateNewProblem()
    
    def Cursor(self, query: str) -> list:
        self.CursorObject.execute(query)
        result = self.CursorObject.fetchall()
        return result
    
    @property
    def Exists(self) -> bool:
        query = f"select userid from user where userid=\"{self.userid}\""
        result = self.Cursor(query)
        if len(result) == 0:
            return False
        else:
            return True
    
    def Create(self) -> None:
        query = f"insert into user (userid) values (\"{self.userid}\")"
        self.Cursor(query)
    
    def GenerateNewProblem(self) -> None:
        operation = self._ChooseOperation()
        match operation:
            case '+':
                answer = randint(1, self.Max_Sum)
                left = randint(1, answer)
                right = answer - left
            case '-':
                left = randint(1, self.Max_Sum)
                right = randint(1, left)
                answer = left - right
            case '*':
                left = randint(1, self.Max_Factor)
                right = randint(1, self.Max_Factor)
                answer = left * right
            case '/':
                right = randint(1, self.Max_Factor)
                answer = randint(1, self.Max_Factor)
                left = answer * right
            case _:
                self.Problem = None
                self.Answer = None
                return
        self.Problem = f"{left} {operation} {right}"
        self.Answer = str(answer)

    def _ChooseOperation(self):
        choices = []
        if self.Addition == True: 
            choices += ['+']
        if self.Subtraction == True:
            choices += ['-']
        if self.Multiplication == True:
            choices += ['*']
        if self.Division == True:
            choices += ['/']
        if len(choices) == 0:
            operation = None
        else:
            operation = choice(choices)
        return operation
    
    def __getitem__(self, field: str) -> any:
        """
        Gets and access to the database through SQL queries. 
        ### Parameters
        - `field`: `str` - name of the column
        """

        query = f"select {field} from user where userid=\"{self.userid}\""
        result = self.Cursor(query)
        value = result[0][0]

        match field:

            case "problem" | "answer":
                return value

            case "addition" | "subtraction" | "multiplication" | "division":
                if value == 0:
                    return False
                elif value == 1:
                    return True
                else:
                    raise ValueError
            
            case "state" | "max_sum" | "max_factor" | "correct" | "incorrect" | "skipped":
                return value
            
            case _:
                raise ValueError

    def __setitem__(self, field: str, value: any) -> None: 

        match field: 

            case "problem" | "answer":
                query = f"update user set {field}=\"{value}\" where userid=\"{self.userid}\""
        
            case "addition" | "subtraction" | "multiplication" | "division":
                if value == True:
                    query = f"update user set {field}=1 where userid=\"{self.userid}\""
                elif value == False:
                    query = f"update user set {field}=0 where userid=\"{self.userid}\""
                else:
                    raise ValueError
            
            case "max_sum" | "max_factor":
                if value <= 0:
                    raise LessThanZeroException
                elif value >= 100:
                    raise ValueTooBigException
                else:
                    query = f"update user set {field}={value} where userid=\"{self.userid}\""    
            
            case "state" | "correct" | "incorrect" | "skipped":
                query = f"update user set {field}={value} where userid=\"{self.userid}\""

            case _:
                raise ValueError
        
        self.Cursor(query)
    
    def GetFormatedSettings(self) -> dict[str, str]:
        settings = {}
        settings['addition'] = f"Addition: {self.Addition}"
        settings['subtraction'] = f"Subtraction: {self.Subtraction}"
        settings['multiplication'] = f"Multiplication: {self.Multiplication}"
        settings['division'] = f"Division: {self.Division}"
        settings['max_sum'] = f"Max sum = {self.Max_Sum}"
        settings['max_factor'] = f"Max factor = {self.Max_Factor}"
        return settings
    
    @property
    def State(self) -> int:
        return self.__getitem__("state")

    @property
    def Problem(self) -> str:
        return self.__getitem__("problem")
    
    @property
    def Answer(self) -> str:
        return self.__getitem__("answer")
    
    @property
    def Addition(self) -> bool: 
        return self.__getitem__("addition")
    
    @property
    def Subtraction(self) -> bool:
        return self.__getitem__("subtraction")
    
    @property
    def Multiplication(self) -> bool:
        return self.__getitem__("multiplication")
    
    @property
    def Division(self) -> bool:
        return self.__getitem__("division")
    
    @property
    def Max_Sum(self) -> int:
        return self.__getitem__("max_sum")
    
    @property
    def Max_Factor(self) -> int:
        return self.__getitem__("max_factor")

    @property
    def Correct(self) -> int:
        return self.__getitem__("correct")
    
    @property
    def Incorrect(self) -> int:
        return self.__getitem__("incorrect")

    @property
    def Skipped(self) -> int:
        return self.__getitem__("skipped")
    
    @State.setter
    def State(self, value: int):
        self.__setitem__("state", value)

    @Problem.setter
    def Problem(self, value: str):
        self.__setitem__("problem", value)
    
    @Answer.setter
    def Answer(self, value: str):
        self.__setitem__("answer", value)
    
    @Addition.setter
    def Addition(self, value: bool):
        self.__setitem__("addition", value)
    
    @Subtraction.setter
    def Subtraction(self, value: bool):
        self.__setitem__("subtraction", value)
    
    @Multiplication.setter
    def Multiplication(self, value: bool):
        self.__setitem__("multiplication", value)
    
    @Division.setter
    def Division(self, value: bool):
        self.__setitem__("division", value)
    
    @Max_Sum.setter
    def Max_Sum(self, value: int):
        self.__setitem__("max_sum", value)
    
    @Max_Factor.setter
    def Max_Factor(self, value: int):
        self.__setitem__("max_factor", value)
    
    @Correct.setter
    def Correct(self, value: int):
        self.__setitem__("correct", value)
    
    @Incorrect.setter
    def Incorrect(self, value: int):
        self.__setitem__("incorrect", value)
    
    @Skipped.setter
    def Skipped(self, value: int):
        self.__setitem__("skipped", value)