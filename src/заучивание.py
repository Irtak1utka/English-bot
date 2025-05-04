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


def random_word_from_list():
    global button_list
    transtation_word = random.choice(list(dictionary.keys()))
    button_list.append(transtation_word)
    bot.send_message(message.chat.id, text=transtation_word)

    button_list.append(dictionary[transtation_word])
    c_distionary = list(dictionary.values()).copy()
    other_3_word = random.choices(c_distionary, 3)
    button_list += other_3_word
    random.shuffle(button_list)


@bot.message_handler(commands=['cards'])
def try_card(message):
    global learning_mode
    learning_mode = True
    random_word_from_list()


@bot.message_handler(content_types='text')
def probably(message):
    global learning_mode, button_list
    if learning_mode:
        if message == "stop":
            learning_mode = False
            exit()
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for el in button_list:
                item_i = types.KeyboardButton(el)
                markup.add(item_i)
    # for i in range(3):
    #     button_list.append(random.choice(list(dictionary.keys())))
    # random.shuffle(button_list)
    # for i in range(4):
    #     item_i = types.KeyboardButton(dictionary[button_list[i]])
    #     markup.add(item_i)


bot.infinity_polling()
