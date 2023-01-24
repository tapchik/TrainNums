from trainnums import TrainNums
import mysql.connector
from user import User

host = "Maxs-MacBook-Air.local"
user = "root"
password = "root"
base = "TrainNums"

database = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password, 
            database=base)

database.autocommit = True

user = User(database, "328")

user.Problem = "10+4"
user.State = 3
user.Answer = "14"
user.Addition = False
user.Subtraction = False
user.Max_Sum = 100

print(user.Addition)
print(user.Problem)
print(user.State)
print(user.Max_Sum)

"""
user["problem"] = "3+9"
user["answer"] = "12"
user["addition"] = True
user["subtraction"] = True
user["multiplication"] = True
user["division"] = True
user["correct"] += 1
"""

"""
print(user["problem"])
print(user["answer"])
print(user["addition"])
print(user["subtraction"])
print(user["multiplication"])
print(user["division"])
print(user["correct"])
"""