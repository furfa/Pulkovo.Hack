import telebot
from telebot import types
import datetime
import config

bot = telebot.TeleBot(config.TOKEN)

temp_register = {}
users = {}
def register(chat_id):
    users[chat_id] = temp_register.get(chat_id)

    return True


remove_keyboard = types.ReplyKeyboardRemove(selective=False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.send_message(message.chat.id, "Это бот, позволяющий отслеживать расписание /reg чтобы получать уведомления о рассписании")
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('/reg')
    itembtn2 = types.KeyboardButton('/get')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Это бот, позволяющий отслеживать расписание:", reply_markup=markup)

@bot.message_handler(commands=['reg'])
def reg(message):
    bot.send_message(message.chat.id,"Введите ФИО",reply_markup=remove_keyboard)
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    question = f"Вы :{message.text}?"
    bot.send_message(message.from_user.id, text=question, reply_markup=markup)

    temp_register[message.chat.id] = message.text

    bot.register_next_step_handler(message, check_name)
def check_name(message):
    if message.text == "Да":
        register(message.chat.id)
        bot.send_message(message.from_user.id, text="Вам будут приходить уведомления о расписании", reply_markup=remove_keyboard)
        return
    bot.send_message(message.from_user.id, text="Для повторной попытки регистрации /reg", reply_markup=remove_keyboard)

@bot.message_handler(content_types=["text"])
def echo(message):
    print(message.text)
    bot.send_message(message.chat.id,"smb")

bot.polling(none_stop=True)
