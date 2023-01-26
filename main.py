import telebot
from telebot import types
import sqlite3
import yaml
from User import User
from User import Task
from User import Settings
import connector
import replies
import trainnums
from custom_exceptions import *

def ReadAssetsFile(assets_file: str) -> dict[str, str]:
    try: 
        read_assets = open(assets_file)
        data_from_assets_file = yaml.safe_load(read_assets)
    except FileNotFoundError:
        raise AssetsFileNotFound("Error. Specified assets file not found. ")
    read_assets.close()
    return data_from_assets_file

assets = ReadAssetsFile("assets.yml")

telegramBotToken = assets["TelegramBotToken"]
bot = telebot.TeleBot(telegramBotToken)

database = sqlite3.connect("trainnums.db", check_same_thread=False)

@bot.inline_handler(lambda query: query.query == 'стих')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Стихотворение', types.InputTextMessageContent('Ехал Грека через реку, видит грека в реке... рак? Или что там было... Я забыла... '))
        r2 = types.InlineQueryResultArticle('2', 'Поэма', types.InputTextMessageContent('Говорят, что время лечит. Нет - не лечит никогда!'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
       print(e)

@bot.message_handler(commands=['start'])
def start(message):
    user: User = connector.LoadInfoAboutUser(database, message.chat.id)
    mess = f"Solve this problem: {user.task.problem}"
    bot.send_message(message.chat.id, mess, parse_mode='html') # 'html' or 'Markdown'

@bot.message_handler(commands=['skip'])
def skip(message):
    user: User = connector.LoadInfoAboutUser(database, message.chat.id)
    user.stats.skipped += 1
    try: 
        user.task = trainnums.GenerateNewProblem(user.settings)
        reply = replies.PresentProblemAfterSkip(user.task)
    except UnableToGenerateProblemException:
        reply = replies.AskToTurnOnAnOperation()
        show_settings(message, text=reply)
        return
    connector.UpdateInfoAboutUser(database, user)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    user: User = connector.LoadInfoAboutUser(database, message.chat.id)
    reply = replies.PresentStats(user.stats)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['settings'])
def show_settings(message, text=replies.PresentSettings()):
    user = connector.LoadInfoAboutUser(database, message.chat.id)
    markup = _MarkupForSettings(user.settings)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
    user = connector.LoadInfoAboutUser(database, str(call.message.chat.id))
    answer = None
    match call.data:
        case "addition_switch":
            user.settings.addition = not user.settings.addition
        case "subtraction_switch":
            user.settings.subtraction = not user.settings.subtraction
        case "multiplication_switch":
            user.settings.multiplication = not user.settings.multiplication
        case "division_switch":
            user.settings.division = not user.settings.division
        case "lessen_max_sum":
            try:
                user.settings.max_sum -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_sum":
            try:
                user.settings.max_sum += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case "lessen_max_factor":
            try:
                user.settings.max_factor -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_factor":
            try:
                user.settings.max_factor += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case _:
            answer = "Unrecognized query"
    
    bot.answer_callback_query(call.id, answer)

    connector.UpdateInfoAboutUser(database, user)

    markup = _MarkupForSettings(user.settings)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)

@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить сайт", url='https://google.com'))
    bot.send_message(message.chat.id, "Перейдите на сайт", reply_markup=markup)

@bot.message_handler(commands=['help'])
def give_help(message):
    #TODO: write helping message
    bot.send_message(message.chat.id, "Сейчас помогу")

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    user = connector.LoadInfoAboutUser(database, message.chat.id)

    if message.text != user.task.answer:
        user.stats.incorrect += 1
        reply = replies.PresentSameProblemAfterFailure(user.task)
        bot.send_message(message.chat.id, reply)
        return
    
    # if text from user is a correct answer
    user.stats.correct += 1
    settings = user.settings
    user.task = Task(None, None)
    try:
        user.task = trainnums.GenerateNewProblem(settings)
        reply = replies.PresentProblemAfterSuccess(user.task)
        reply = replies.PresentProblemAfterSuccess(user.task)
        bot.send_message(message.chat.id, reply)
    except UnableToGenerateProblemException:
        reply = replies.InformAboutSuccess()
        bot.send_message(message.chat.id, reply)
        reply = replies.AskToTurnOnAnOperation()
        show_settings(message, text=reply)
    finally:
        connector.UpdateInfoAboutUser(database, user)

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
