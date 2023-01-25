import telebot
from telebot import types
import sqlite3
import yaml
from User import User
import connector
import trainnums
from custom_exceptions import *

def ReadAssetsFile(assets_file: str) -> dict[str, str]:
    try: 
        read_assets = open(assets_file)
        #with open(assets_file) as read_assets:
        data_from_assets_file = yaml.safe_load(read_assets)
        #telegramBotToken: str = read_data["TelegramBotToken"]
    except FileNotFoundError:
        raise AssetsFileNotFound("Error. Specified assets file not found. ")
    finally:
        read_assets.close()
    return data_from_assets_file

assets = ReadAssetsFile("assets.yml")

telegramBotToken = assets["TelegramBotToken"]
bot = telebot.TeleBot(telegramBotToken)

database = sqlite3.connect("database.db", check_same_thread=False)

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
    mess = f"Solve this problem: {user.problem}"
    bot.send_message(message.chat.id, mess, parse_mode='html') # 'html' or 'Markdown'

@bot.message_handler(commands=['skip'])
def start(message):
    user: User = connector.LoadInfoAboutUser(database, message.chat.id)
    user.skipped += 1
    user_settings = user.extract_settings()
    user.problem, user.answer = trainnums.GenerateNewProblem(user_settings)
    reply = f"Ok\nHere is another one {user.problem}"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    user = connector.LoadInfoAboutUser(database, message.chat.id)
    reply = (f"Here are your stats:\n" 
            + f"Correct: {user.correct}\n"
            + f"Incorrect: {user.incorrect}\n"
            + f"Skipped: {user.skipped}\n")
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['settings'])
def show_settings(message):
    user = connector.LoadInfoAboutUser(database, message.chat.id)
    markup = _MarkupForSettings(user)
    bot.send_message(message.chat.id, "Here are your settings: ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
    user = connector.LoadInfoAboutUser(database, call.message.chat.id)
    answer = None
    match call.data:
        case "addition_switch":
            user.addition = not user.addition
        case "subtraction_switch":
            user.subtraction = not user.subtraction
        case "multiplication_switch":
            user.multiplication = not user.multiplication
        case "division_switch":
            user.division = not user.division
        case "lessen_max_sum":
            try:
                user.max_sum -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_sum":
            try:
                user.max_sum += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case "lessen_max_factor":
            try:
                user.max_factor -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_factor":
            try:
                user.max_factor += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case _:
            answer = "Unrecognized query"
    
    bot.answer_callback_query(call.id, answer)

    connector.UpdateInfoAboutUser(database, user)
    database.commit()

    markup = _MarkupForSettings(user)
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
    if message.text == user.answer:
        user.correct += 1
        settings = user.extract_settings()
        user.problem, user.answer = trainnums.GenerateNewProblem(settings)
        connector.UpdateInfoAboutUser(database, user)
        database.commit()
        reply = f"Correct!\nHere is another one: {user.problem}"
    else:
        user.incorrect += 1
        reply = f"Incorrect!\nTry some more: {user.problem}"
    bot.send_message(message.chat.id, reply)

def _MarkupForSettings(user: User) -> types.ReplyKeyboardMarkup: 
    row1 = [types.InlineKeyboardButton(f"Addition: {user.addition}", callback_data="addition_switch"),
            types.InlineKeyboardButton(f"Multiplication: {user.multiplication}", callback_data="multiplication_switch")]
    row2 = [types.InlineKeyboardButton(f"Subtraction: {user.subtraction}", callback_data="subtraction_switch"),
            types.InlineKeyboardButton(f"Division: {user.division}", callback_data="division_switch")]
    row3 = [types.InlineKeyboardButton(f"-", callback_data="lessen_max_sum"),
            types.InlineKeyboardButton(f"Max sum = {user.max_sum}", callback_data="max_sum"),
            types.InlineKeyboardButton(f"+", callback_data="highten_max_sum")]
    row4 = [types.InlineKeyboardButton(f"-", callback_data="lessen_max_factor"),
            types.InlineKeyboardButton(f"Max factor = {user.max_factor}", callback_data="max_factor"),
            types.InlineKeyboardButton(f"+", callback_data="highten_max_factor")]
    markup = types.InlineKeyboardMarkup([row1, row2, row3, row4])
    return markup

bot.polling(non_stop=True)
