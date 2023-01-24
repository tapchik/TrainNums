
import telebot
from telebot import types
import mysql.connector
from user import User
from custom_exceptions import *

bot = telebot.TeleBot('463906818:AAFXd3k6J98ZpYEDWEIyhwLyBZeJnI-ROq0')

database = mysql.connector.connect(
            host="Maxs-MacBook-Air.local", 
            user="root", 
            password="root", 
            database="TrainNums")
database.autocommit = True

@bot.inline_handler(lambda query: query.query == 'стих')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Стихотворение', types.InputTextMessageContent('Ехал Грека через реку, видит грека в реке... рак? Или что там было... Я забыла... '))
        r2 = types.InlineQueryResultArticle('2', 'Поэма', types.InputTextMessageContent('Говорят, что время лечит. Нет - не лечит никогда!'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
       print(e)
    #if inline_query == 'data':
    #    bot.send_message(message.chat.id, "Ну вот мы и встретились", parse_mode='html') # 'html' or 'Markdown'
    #else:
    #    bot.send_message(message.chat.id, "Ну вот мы и встретились", parse_mode='html') # 'html' or 'Markdown'

@bot.message_handler(commands=['start'])
def start(message):
    user = User(database, str(message.chat.id))
    mess = f'Solve this problem: {user.Problem}'
    bot.send_message(message.chat.id, mess, parse_mode='html') # 'html' or 'Markdown'

@bot.message_handler(commands=['skip'])
def start(message):
    user = User(database, str(message.chat.id))
    user.Skipped += 1
    user.GenerateNewProblem()
    reply = f"Ok\nHere is another one {user.Problem}"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    user = User(database, str(message.chat.id))
    reply = (f"Here are your stats:\n" 
            + f"Correct: {user.Correct}\n"
            + f"Incorrect: {user.Incorrect}\n"
            + f"Skipped: {user.Skipped}\n")
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['settings'])
def show_settings(message):
    user = User(database, str(message.chat.id))
    markup = _MarkupForSettings(user)
    bot.send_message(message.chat.id, "Here are your settings: ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
    user = User(database, call.message.chat.id)
    answer = None
    match call.data:
        case "addition_switch":
            user.Addition = not user.Addition
        case "subtraction_switch":
            user.Subtraction = not user.Subtraction
        case "multiplication_switch":
            user.Multiplication = not user.Multiplication
        case "division_switch":
            user.Division = not user.Division
        case "lessen_max_sum":
            try:
                user.Max_Sum -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_sum":
            try:
                user.Max_Sum += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"
        case "lessen_max_factor":
            try:
                user.Max_Factor -= 10
            except LessThanZeroException:
                answer = "Value can't be zero or less"
        case "highten_max_factor":
            try:
                user.Max_Factor += 10
            except ValueTooBigException:
                answer = "Value reached it's max limit"

        case _:
            answer = "Unrecognized query"
    bot.answer_callback_query(call.id, answer)
    
    markup = _MarkupForSettings(user)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)

@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить сайт", url='https://google.com'))
    bot.send_message(message.chat.id, "Перейдите на сайт", reply_markup=markup)

@bot.message_handler(commands=['settings'])
def settings(message):
    #TODO: markup buttons
    pass

@bot.message_handler(commands=['help'])
def give_help(message):
    #TODO: write helping message
    bot.send_message(message.chat.id, "Сейчас помогу")

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    user = User(database, str(message.chat.id))
    if message.text == user.Answer:
        user.GenerateNewProblem()
        reply = f"Correct!\nHere is another one: {user.Problem}"
        user.Correct += 1
    else:
        reply = f"Incorrect!\nTry some more: {user.Problem}"
        user.Incorrect += 1
    bot.send_message(message.chat.id, reply)

def _MarkupForSettings(user: User) -> types.ReplyKeyboardMarkup: 
    row1 = [types.InlineKeyboardButton(f"Addition: {user.Addition}", callback_data="addition_switch"),
            types.InlineKeyboardButton(f"Multiplication: {user.Multiplication}", callback_data="multiplication_switch")]
    row2 = [types.InlineKeyboardButton(f"Subtraction: {user.Subtraction}", callback_data="subtraction_switch"),
            types.InlineKeyboardButton(f"Division: {user.Division}", callback_data="division_switch")]
    row3 = [types.InlineKeyboardButton(f"-", callback_data="lessen_max_sum"),
            types.InlineKeyboardButton(f"Max sum = {user.Max_Sum}", callback_data="max_sum"),
            types.InlineKeyboardButton(f"+", callback_data="highten_max_sum")]
    row4 = [types.InlineKeyboardButton(f"-", callback_data="lessen_max_factor"),
            types.InlineKeyboardButton(f"Max factor = {user.Max_Factor}", callback_data="max_factor"),
            types.InlineKeyboardButton(f"+", callback_data="highten_max_factor")]
    markup = types.InlineKeyboardMarkup([row1, row2, row3, row4])
    return markup

bot.polling(non_stop=True)
