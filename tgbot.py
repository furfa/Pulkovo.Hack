import telebot
from telebot import types
import datetime
import config

bot = telebot.TeleBot(config.TOKEN)

users = dict()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Это бот, позволяющий отслеживать расписание")
    bot.send_message(message.chat.id,"Введите ФИО")
    
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    users[message.chat.id] = message.text

    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f"Вы :{message.text}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print(inline_query)



@bot.message_handler(func=lambda message: message.text=="xui")
def echo_all(message):
    print(message.text)
    bot.reply_to(message, "Сам xui")

@bot.message_handler(content_types=["text"])
def echo(message):
    print(message.text)

    bot.send_message(message.chat.id,"xui")

bot.polling(none_stop=True)
