from random import choice, randint
from user_settings import user_settings

def GenerateNewProblem(settings: user_settings) -> tuple[str]:
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
            return None, None
    problem = f"{left} {operation} {right}"
    return problem, answer

def ChooseOperation(settings: user_settings) -> str:
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