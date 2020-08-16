import telebot
from telebot import types
import datetime
import config
import json
import os
import pandas as pd
from datetime import datetime
import schedule
import time
from multiprocessing import Process

bot = telebot.TeleBot(config.TOKEN)

temp_register = {}
users = {}

if os.path.exists("users.json"):
    users = json.loads(
        open("users.json", "r").read()
    )

def register(chat_id):
    users[chat_id] = temp_register.get(chat_id)

    with open("users.json", "w") as file:
        file.write(
            json.dumps(
                users,
                ensure_ascii=False,
                indent=4
            )
        )

    return True

def modification_date(raw_filename):
    return os.path.getmtime(raw_filename)

def get_last_schedule():
    
    folder = "RESULT"

    states = [os.path.join(folder,state) for state in os.listdir( folder )]

    last_state = max(states, key=lambda x:modification_date(x))
    print("loading last_file:", last_state)

    return last_state

def check_next_pair(name):
    excel = pd.read_excel( get_last_schedule() )
    try:
        next_pair_df = excel[excel["teacher.name"] == name][ excel["time.start"] >= datetime.now() ][:1]  
    except:
        return "Вы не найдены в расписании"

    message = """
    Следующее, что вы ведете:

    11:30
    Программа дополнительной подготовки водителей спецтранспорта с правом подъезда к воздушному в контролируемой зоне аэродрома «Пулково». 
    Аудитория: БАТО,213 """

    return message #str( next_pair_df.values[0] )

remove_keyboard = types.ReplyKeyboardRemove(selective=False)

def get_main_keyboard(chat_id = None):
    markup = types.ReplyKeyboardMarkup()
    if chat_id in users.keys():
        itembtn1 = types.KeyboardButton('/reg Посмотреть что вести следующим уроком')
    else:
        itembtn1 = types.KeyboardButton('/reg для ежедневных уведомлений')

    itembtn2 = types.KeyboardButton('/get получить полное расписание')
    markup.add(itembtn1, itembtn2)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.send_message(message.chat.id, "Это бот, позволяющий отслеживать расписание /reg чтобы получать уведомления о рассписании")
    markup = get_main_keyboard(message.chat.id)
    bot.send_message(message.chat.id, "Это бот, позволяющий отслеживать расписание:", reply_markup=markup)

@bot.message_handler(commands=['get'])
def reg(message):
    with open(get_last_schedule(), "rb") as file:
        bot.send_document(message.chat.id, file)

    bot.send_message(message.chat.id,"файл отправлен")

@bot.message_handler(commands=['reg'])
def reg(message):

    if message.chat.id in users.keys():
        bot.send_message(message.chat.id, check_next_pair(users[message.chat.id]) )
        return 
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
        bot.send_message(message.from_user.id, text="Вам будут приходить уведомления о расписании", reply_markup=get_main_keyboard(message.chat.id))
        return
    bot.send_message(message.from_user.id, text="Для повторной попытки регистрации /reg", reply_markup=get_main_keyboard(message.chat.id))

@bot.message_handler(content_types=["text"])
def echo(message):
    print(message.text)
    bot.send_message(message.chat.id,"Такой команды нет (")

# это функция отправки сообщений по таймеру
def check_send_messages():
    while True:
        # ваш код проверки времени и отправки сообщений по таймеру
        # пауза между проверками, чтобы не загружать процессор
        for k, v in users.items():
            bot.send_message(k, check_next_pair(v))
        time.sleep(60)
  
# а теперь запускаем проверку в отдельном потоке
p1 = Process(target=check_send_messages, args=())
p1.start()


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            # повторяем через 15 секунд в случае недоступности сервера Telegram
            time.sleep(15)
