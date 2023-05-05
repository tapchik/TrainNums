from random import choice, randint
from User import Task
from User import Settings
import custom_exceptions

def GenerateNewProblem(settings: Settings) -> Task:
    operation = ChooseOperation(settings)
    match operation:
        case '+':
            answer = randint(1, settings.max_sum)
            left = randint(1, answer)
            right = answer - left
        case '-':
            left = randint(1, settings.max_sum)
            right = randint(1, left)
            answer = left - right
        case '*':
            left = randint(1, settings.max_factor)
            right = randint(1, settings.max_factor)
            answer = left * right
        case '/':
            right = randint(1, settings.max_factor)
            answer = randint(1, settings.max_factor)
            left = answer * right
        case _:
            raise custom_exceptions.UnableToGenerateProblemException
    problem = f"{left} {operation} {right}"
    task = Task(problem, str(answer))
    return task

def ChooseOperation(settings: Settings) -> str | None:
    choices = []
    if settings.addition == True: 
        choices += ['+']
    if settings.subtraction == True:
        choices += ['-']
    if settings.multiplication == True:
        choices += ['*']
    if settings.division == True:
        choices += ['/']
    if len(choices) == 0:
        operation = None
    else:
        operation = choice(choices)
    return operation