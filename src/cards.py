import telebot
from telebot import types
import json
import random
from main import bot_token

bot = telebot.TeleBot(bot_token)
learning_mode = False
button_list = []

with open("words.json", encoding="UTF-8") as e:
    dictionary = json.load(e)

print(dictionary)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['cards'])
def try_card(message):
    global learning_mode
    learning_mode = True
    a = random.choice(list(dictionary.keys()))
    button_list.append(a)
    bot.send_message(message.chat.id, text=a)


@bot.message_handler(content_types='text')
def probably(message):
    global learning_mode, button_list
    if learning_mode:
        if message == "stop":
            learning_mode = False
            exit()
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(3):
                button_list.append(random.choice(list(dictionary.keys())))
            random.shuffle(button_list)
            for i in range(4):
                item_i = types.KeyboardButton(dictionary[button_list[i]])
                markup.add(item_i)

bot.infinity_polling()
