import telebot
from telebot import types
import datetime
import config

bot = telebot.TeleBot(config.TOKEN)

users = {}
def register(chat_id, name):
    users[chat_id] = name

    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Это бот, позволяющий отслеживать расписание /reg чтобы получать уведомления о рассписании")

@bot.message_handler(commands=['reg'])
def reg(message):
    bot.send_message(message.chat.id,"Введите ФИО")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f"Вы :{message.text}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "yes":
            register(call.message.chat.id, call.message.text[4:][:-1])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Зарегистрирован")

        if call.data == "no":
            # bot.register_next_step_handler(, reg)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Напишите /reg, чтобы исправить")


@bot.message_handler(content_types=["text"])
def echo(message):
    print(message.text)
    bot.send_message(message.chat.id,"smb")

bot.polling(none_stop=True)
