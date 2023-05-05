import models

def PresentProblemAfterSkip(task: models.Task) -> str:
    message = f"Ok\nSolve this one instead: {task.problem}"
    return message

def PresentProblemAfterSuccess(task: models.Task) -> str:
    message = f"Correct!\nHere is another one: {task.problem}"
    return message

def PresentSameProblemAfterFailure(task: models.Task) -> str:
    message = f"Incorrect!\nTry some more: {task.problem}"
    return message

def PresentSameProblemAfterSettings(task: models.Task) -> str:
    message = f"Ok, settings saved, but solve previous problem first: {task.problem}"
    return message

def InformAboutSuccess() -> str:
    message = "Well done, that is correct!"
    return message

def PresentStats(stats: models.Stats) -> str:
    message = (f"Here are your stats:\n" + \
               f"Correct: {stats.correct}\n" + \
               f"Incorrect: {stats.incorrect}\n" + \
               f"Skipped: {stats.skipped}\n")
    return message

def PresentSettings():
    message = "Here are your settings: "
    return message

def AskToTurnOnAnOperation():
    message = "Sorry mate, turn back on at least one operation so I can generate a problem for you:"
    return message