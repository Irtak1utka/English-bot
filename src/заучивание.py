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


def random_word_from_list(message):
    global button_list
    transtation_word = random.choice(list(dictionary.keys()))
    button_list.append(transtation_word)
    bot.send_message(message.chat.id, text=transtation_word)
    print(transtation_word)

    button_list.append(dictionary[transtation_word])
    c_distionary = list(dictionary.values()).copy()
    other_3_word = random.choices(c_distionary, k=3)
    button_list += other_3_word
    random.shuffle(button_list)

    answer_is_correct(message)


def answer_is_correct(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for el in button_list:
        item_i = types.KeyboardButton(el)
        markup.add(item_i)
    bot.send_message(message.chat.id, 'Выберите верный вариант', reply_markup=markup)


@bot.message_handler(commands=['learn'])
def try_card(message):
    global learning_mode
    learning_mode = True
    random_word_from_list(message)


@bot.message_handler(commands=['cards'])
def cards(message):
    for el in dictionary:
        bot.send_message(message.chat.id, f"{el} - <tg-spoiler>{dictionary[el]}</tg-spoiler>")
        print(el)


@bot.message_handler(content_types='text')
def probably(message):
    global learning_mode, button_list
    if learning_mode:
        if message == "stop":
            learning_mode = False
            exit()
        # else:
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # for el in button_list:
            #     item_i = types.KeyboardButton(el)
            #     markup.add(item_i)
            # bot.send_message(message.chat.id, 'Выберите верный вариант', reply_markup=markup)


bot.infinity_polling()
