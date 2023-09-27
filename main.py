import telebot
from telebot import types
import sqlite3
import utils
from models import Task, Settings, User, Stats
import connector
from connector import Connector
import replies
import generate
from custom_exceptions import *

# init
assets = utils.ReadAssetsFile('assets.yml')
bot = telebot.TeleBot(assets['TelegramBotToken'])
database = sqlite3.connect(assets['DatabaseMaster'], check_same_thread=False)
del(assets)

connector = Connector(database)

@bot.inline_handler(lambda query: query.query == 'стих')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Стихотворение', types.InputTextMessageContent('Ехал Грека через реку, видит грека в реке... рак? Или что там было... Я забыла... '))
        r2 = types.InlineQueryResultArticle('2', 'Поэма', types.InputTextMessageContent('Говорят, что время лечит. Нет - не лечит никогда!'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
       print(e)

@bot.message_handler(commands=['start'])
def handle_start(message):
    task = connector.GetTask(message.chat.id)
    if task.problem == None: 
        task = connector.GenerateNextTask(message.chat.id)
    if task.problem == None:
        InformUnableToGenerate(message)
        return
    reply = f"Solve this problem: {task.problem}"
    bot.send_message(message.chat.id, reply, parse_mode='html') # 'html' or 'Markdown'

@bot.message_handler(commands=['skip'])
def skip(message):
    task = connector.GetTask(message.chat.id)
    settings = connector.GetSettings(message.chat.id)
    stats = connector.GetStats(message.chat.id)
    stats.skipped += 1
    if connector.AbleToGenerateNewProblem(message.chat.id): 
        task = generate.newProblem(settings)
        reply = replies.PresentProblemAfterSkip(task)
    else:
        reply = replies.AskToTurnOnAnOperation()
        show_settings(message, text=reply)
        return
    bot.send_message(message.chat.id, reply)
    connector.Save(message.chat.id, task)
    connector.Save(message.chat.id, settings)
    connector.Save(message.chat.id, stats)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    stats = connector.GetStats(message.chat.id)
    reply = replies.PresentStats(stats)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['settings'])
def show_settings(message, text=replies.PresentSettings()):
    settings = connector.GetSettings(message.chat.id)
    markup = _MarkupForSettings(settings)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
    user_id = str(call.message.chat.id)
    settings = connector.GetSettings(user_id)
    answer = None
    match call.data:
        case "addition_switch":
            settings.addition = not settings.addition
        case "subtraction_switch":
            settings.subtraction = not settings.subtraction
        case "multiplication_switch":
            settings.multiplication = not settings.multiplication
        case "division_switch":
            settings.division = not settings.division
        case "lessen_max_sum":
            try:
                settings.max_sum -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_sum":
            try:
                settings.max_sum += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case "lessen_max_factor":
            try:
                settings.max_factor -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_factor":
            try:
                settings.max_factor += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case _:
            answer = "Unrecognized query"
    
    bot.answer_callback_query(call.id, answer)

    connector.Save(user_id, settings)

    markup = _MarkupForSettings(settings)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):

    task = connector.GetTask(message.chat.id)
    settings = connector.GetSettings(message.chat.id)
    stats = connector.GetStats(message.chat.id)

    success = False
    if message.text == task.answer:
        stats.correct += 1
        success = True
    else: # message.text != task.answer
        stats.incorrect += 1
        success = False
    
    if success==False:
        reply = replies.PresentSameProblemAfterFailure(task)
    elif success==True and connector.AbleToGenerateNewProblem(message.chat.id):
        task = generate.newProblem(settings)
        reply = replies.PresentProblemAfterSuccess(task)
    elif success==True and connector.AbleToGenerateNewProblem(message.chat.id)==False: 
        reply = replies.InformAboutSuccess()
        reply = replies.AskToTurnOnAnOperation()
        show_settings(message, text=reply)

    bot.send_message(message.chat.id, reply)
    connector.Save(message.chat.id, task)
    connector.Save(message.chat.id, settings)
    connector.Save(message.chat.id, stats)

def InformUnableToGenerate(message):
    reply = replies.AskToTurnOnAnOperation()
    show_settings(message, text=reply)

def _MarkupForSettings(settings: Settings) -> types.InlineKeyboardMarkup: 
    row1 = [types.InlineKeyboardButton(f"Addition: {settings.addition}", callback_data="addition_switch"),
            types.InlineKeyboardButton(f"Multiplication: {settings.multiplication}", callback_data="multiplication_switch")]
    row2 = [types.InlineKeyboardButton(f"Subtraction: {settings.subtraction}", callback_data="subtraction_switch"),
            types.InlineKeyboardButton(f"Division: {settings.division}", callback_data="division_switch")]
    row3 = [types.InlineKeyboardButton(f"-", callback_data="lessen_max_sum"),
            types.InlineKeyboardButton(f"Max sum = {settings.max_sum}", callback_data="max_sum"),
            types.InlineKeyboardButton(f"+", callback_data="highten_max_sum")]
    row4 = [types.InlineKeyboardButton(f"-", callback_data="lessen_max_factor"),
            types.InlineKeyboardButton(f"Max factor = {settings.max_factor}", callback_data="max_factor"),
            types.InlineKeyboardButton(f"+", callback_data="highten_max_factor")]
    markup = types.InlineKeyboardMarkup([row1, row2, row3, row4])
    return markup

bot.polling(non_stop=True)
