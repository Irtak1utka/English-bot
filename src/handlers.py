import datetime
import io
import os
import random
import re  # Import the regular expression module

from telethon import events, Button
# from telethon.tl.functions.channels.delete_messages import DeleteMessagesRequest
from PIL import Image

from db_models import UserTg, UserBot, Card, Collection, Review
from utils import hash_password, is_password_strong, generate_unique_module_id
from keyboards import create_main_menu_keyboard, create_back_to_main_menu_keyboard, \
    create_language_selection_keyboard, create_my_account_keyboard, \
    create_language_selection_keyboard_with_back, create_add_cards_keyboard, create_add_image_keyboard, \
    create_card_saved_keyboard, create_learning_menu_keyboard, create_edit_modules_keyboard, create_module_keyboard
from localization import get_text, translate_images

# Состояния
registration_state = {}
change_nickname_state = {}
change_password_state = {}
activate_premium_state = {}
password_required_after_menu = {}
module_creation_state = {}
card_creation_state = {}
module_view_state = {}
card_message_ids = {}
find_landuage = ""

CARDS_FOLDER = "cards_folder"

language_codes = {
    'ru': 'ru',
    'en': 'en',
    'uk': 'ukr',
    'pl': 'pol',
    'zh': 'chin',
    'ja': 'jap'
}


def register_handlers(client, Session, NON_IMAGE_PATH, MAIN_MENU_IMG_PATH, STARS_LEARN_IMG_PATH, CREATE_NEW_IMG_PATH,
                      INFO_IMG_PATH, HOW_TO_USE_IMG_PATH, MY_ACC_IMG_PATH):
    # Общие обработчики (можно вынести в отдельный файл)
    @client.on(events.CallbackQuery(data=b"my_account"))
    async def my_account_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        user_bot = session.query(UserBot).filter_by(id=user_id).first()

        if not user_bot:
            await event.answer("Пожалуйста, зарегистрируйтесь, прежде чем использовать эту функцию.")
            return

        nick = user_bot.nick
        date = user_tg.date.strftime("%d.%m.%Y") if user_tg.date else "0"
        count_of_cards = user_bot.count_of_cards

        reviews = session.query(Review).filter_by(id_to=user_id).all()
        if reviews:
            total_score = sum(review.score for review in reviews)
            rating = round(total_score / len(reviews), 2)
        else:
            rating = "0"

        premium_date = user_bot.premium.strftime("%d.%m.%Y") if user_bot.premium else "0"

        account_info = get_text(language, 'my_account_info', user_id, nick, date, count_of_cards, rating,
                                premium_date)

        await client.edit_message(event.chat_id, event.message_id, account_info,
                                  buttons=create_my_account_keyboard(language), file=MY_ACC_IMG_PATH)

        # await client.delete_messages(event.chat_id, event.message_id)
        session.close()

    @client.on(events.CallbackQuery(data=b"change_language"))
    async def change_language_handler(event):
        # global find_landuage
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        # find_landuage = language
        # print(language)
        await event.edit(get_text(language, 'change_language'), buttons=create_language_selection_keyboard())
        session.close()

    @client.on(events.CallbackQuery(pattern=b"lang_.*"))
    async def language_selection_handler(event):
        # global CARDS_FOLDER, USUAL_IMG_FOLDER, NON_IMAGE_PATH, \
        #     MAIN_MENU_IMG_PATH, STARS_LEARN_IMG_PATH, CREATE_NEW_IMG_PATH, INFO_IMG_PATH, \
        #     HOW_TO_USE_IMG_PATH, MY_ACC_IMG_PATH
        session = Session()
        user_id = event.sender_id
        language = event.data.decode('utf-8').split('_')[1]
        # print(language, 333)
        # print(CREATE_NEW_IMG_PATH, "handler1")
        # translate_images(language)
        # print(CREATE_NEW_IMG_PATH, "handler2")
        user_tg = session.query(UserTg).filter_by(id=user_id).first()

        if not user_tg:
            # Если нет информации о пользователе, создаем
            user_tg = UserTg(id=user_id, username=event.sender.username or "NO_USERNAME",
                             date=datetime.datetime.now())
            session.add(user_tg)
            session.commit()

        user_tg.language = language
        session.commit()

        user_bot = session.query(UserBot).filter_by(id=user_id).first()
        if user_bot:
            await send_main_menu(event)
        else:
            # Отправляем новое сообщение с предложением зарегистрироваться
            await client.edit_message(event.chat_id, event.message_id, get_text(language, 'register_message'),
                                      buttons=[[Button.inline(get_text(language, 'register'), data=b"Register")]])
        session.close()

    @client.on(events.CallbackQuery(pattern=b"module_lang_.*"))
    async def module_language_selection_handler(event):
        session = Session()
        user_id = event.sender_id
        language_code = event.data.decode('utf-8').split('_')[2]  # Получаем только код языка
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'  # Получаем язык интерфейса пользователя

        if user_id in module_creation_state:
            if module_creation_state[user_id]["state"] == "waiting_for_original_language":
                module_creation_state[user_id]["lang1"] = language_codes.get(language_code, language_code)
                module_creation_state[user_id]["state"] = "waiting_for_translation_language"

                await event.edit(get_text(language, 'select_translation_language'),
                                 buttons=[
                                     [Button.inline("🇷🇺 Русский", data=b"module_lang_ru"),
                                      Button.inline("🇬🇧 English", data=b"module_lang_en")],
                                     [Button.inline("🇺🇦 Українська", data=b"module_lang_uk"),
                                      Button.inline("🇵🇱 Polski", data=b"module_lang_pl")],
                                     [Button.inline("🇨🇳 中文", data=b"module_lang_zh"),
                                      Button.inline("🇯🇵 日本語", data=b"module_lang_ja")],
                                     [Button.inline("⬅ Назад в главное меню", data=b"back_to_main_menu")]
                                 ])


            elif module_creation_state[user_id]["state"] == "waiting_for_translation_language":
                module_creation_state[user_id]["lang2"] = language_codes.get(language_code, language_code)
                module_creation_state[user_id]["state"] = "waiting_for_module_name"

                await event.edit(get_text(language, 'enter_module_name'),
                                 buttons=create_back_to_main_menu_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(data=b"start_learning"))
    async def start_learning_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        await client.edit_message(event.chat_id, event.message_id, get_text(language, 'start_learning_message'),
                                  buttons=create_learning_menu_keyboard(language), file=STARS_LEARN_IMG_PATH)
        session.close()

    @client.on(events.CallbackQuery(data=b"how_to_use"))
    async def how_to_use_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        await client.edit_message(event.chat_id, event.message_id, get_text(language, 'how_to_use_info'),
                                  buttons=[[Button.url(get_text(language, 'support'), url='https://t.me/telegram')],
                                           create_back_to_main_menu_keyboard(language)[0]], file=HOW_TO_USE_IMG_PATH)
        session.close()

    @client.on(events.CallbackQuery(data=b"create_module"))
    async def edit_modules_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        await client.edit_message(event.chat_id, event.message_id, get_text(language, 'edit_modules_message'),
                                  buttons=create_edit_modules_keyboard(language), file=CREATE_NEW_IMG_PATH)
        session.close()

    @client.on(events.CallbackQuery(data=b"add_cards_action"))  # Изменено data
    async def add_cards_action_handler(event):  # Переименовано название функции
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        if user_id in card_creation_state:
            # Устанавливаем состояние ожидания ввода иностранного слова
            card_creation_state[user_id]["state"] = "waiting_for_foreign_word"
            # await event.edit(event.chat_id, event.message_id, get_text(language, 'enter_foreign_word')) #  Заменено
            await client.send_message(event.chat_id,
                                      get_text(language, 'enter_foreign_word'))  # Отправляем новое сообщение
        session.close()

    @client.on(events.CallbackQuery(data=b"bot_info"))
    async def bot_info_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        await client.edit_message(event.chat_id, event.message_id, get_text(language, 'bot_info_message'),
                                  buttons=create_back_to_main_menu_keyboard(language), file=INFO_IMG_PATH)
        session.close()

    @client.on(events.CallbackQuery(data=b"back_to_main_menu"))
    async def back_to_main_menu_handler(event):
        await send_main_menu(event)

    async def send_main_menu(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        await client.edit_message(event.chat_id, event.message_id, get_text(language, 'main_menu'),
                                  buttons=create_main_menu_keyboard(language), file=MAIN_MENU_IMG_PATH)
        session.close()

    @client.on(events.CallbackQuery(data=b"create_module"))
    async def create_module_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        # Инициализируем состояние создания модуля
        module_creation_state[user_id] = {"state": "waiting_for_original_language"}

        # Отправляем сообщение с запросом выбора языка оригинала, используя НОВЫЙ обработчик
        await event.edit(get_text(language, 'select_original_language'),
                         buttons=[
                             [Button.inline("🇷🇺 Русский", data=b"module_lang_ru"),
                              Button.inline("🇬🇧 English", data=b"module_lang_en")],
                             [Button.inline("🇺🇦 Українська", data=b"module_lang_uk"),
                              Button.inline("🇵🇱 Polski", data=b"module_lang_pl")],
                             [Button.inline("🇨🇳 中文", data=b"module_lang_zh"),
                              Button.inline("🇯🇵 日本語", data=b"module_lang_ja")],
                             [Button.inline("⬅ Назад в главное меню", data=b"back_to_main_menu")]
                         ])
        session.close()

    @client.on(events.CallbackQuery(pattern=b"lang_.*"))
    async def language_selection_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        selected_language = event.data.decode('utf-8').split('_')[1]

        if user_id in module_creation_state:
            if module_creation_state[user_id]["state"] == "waiting_for_original_language":
                module_creation_state[user_id]["lang1"] = language_codes.get(selected_language, selected_language)
                module_creation_state[user_id]["state"] = "waiting_for_translation_language"

                # Отправляем сообщение с запросом выбора языка перевода
                await client.edit_message(event.chat_id, event.message_id,
                                          get_text(language, 'select_translation_language'),
                                          buttons=create_language_selection_keyboard_with_back())

            elif module_creation_state[user_id]["state"] == "waiting_for_translation_language":
                module_creation_state[user_id]["lang2"] = language_codes.get(selected_language, selected_language)
                module_creation_state[user_id]["state"] = "waiting_for_module_name"

                # Запрашиваем название модуля
                await event.edit(event.chat_id, event.message_id, get_text(language, 'enter_module_name'),
                                 buttons=create_back_to_main_menu_keyboard(language))

        else:
            # Обработка выбора языка для других целей (например, смена языка бота)
            user_tg = session.query(UserTg).filter_by(id=user_id).first()
            if user_tg:
                user_tg.language = selected_language
                session.commit()
                user_bot = session.query(UserBot).filter_by(id=user_id).first()

                if user_bot:
                    await send_main_menu(event)
                else:
                    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'register_message'),
                                              buttons=[
                                                  [Button.inline(get_text(language, 'register'), data=b"Register")]])
        session.close()

    @client.on(events.NewMessage)
    async def handle_messages(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        text = event.text

        if user_id in registration_state:
            if registration_state[user_id] == "waiting_for_nickname":
                existing_user = session.query(UserBot).filter_by(nick=text).first()
                if existing_user:
                    await event.respond(get_text(language, 'nickname_taken'))
                    return

                registration_state[user_id] = {"nickname": text,
                                               "state": "waiting_for_password"}

                await event.respond(get_text(language, 'password_request'))

            elif registration_state[user_id].get("state") == "waiting_for_password":
                is_strong, message = is_password_strong(text)
                if not is_strong:
                    await event.respond(
                        f"Пароль не соответствует требованиям: {message} Пожалуйста, повторите ввод пароля:")
                    return

                hashed_password = hash_password(text)

                new_user_bot = UserBot(id=user_id, nick=registration_state[user_id]["nickname"],
                                       pass_hash=hashed_password)
                session.add(new_user_bot)
                session.commit()

                del registration_state[user_id]

                language = user_tg.language  # Получаем язык пользователя
                await send_main_menu_new_message(event)
                await event.delete()

        elif user_id in change_nickname_state:
            if change_nickname_state[user_id] == "waiting_for_new_nickname":
                existing_user = session.query(UserBot).filter_by(nick=text).first()
                if existing_user:
                    await event.respond(get_text(language, 'nickname_exists'))
                    return

                user_bot = session.query(UserBot).filter_by(id=user_id).first()
                user_bot.nick = text
                session.commit()

                del change_nickname_state[user_id]

                await event.respond(get_text(language, 'nickname_changed'),
                                    buttons=create_back_to_main_menu_keyboard(language))

        elif user_id in change_password_state:
            if change_password_state[user_id] == "waiting_for_old_password":
                user_bot = session.query(UserBot).filter_by(id=user_id).first()
                hashed_password = hash_password(text)

                if user_bot.pass_hash != hashed_password:
                    await event.respond(get_text(language, 'incorrect_password'))
                    return

                change_password_state[user_id] = "waiting_for_new_password"
                password_required_after_menu[user_id] = True
                await event.respond(get_text(language, 'enter_new_password'))

            elif change_password_state[user_id] == "waiting_for_new_password":
                is_strong, message = is_password_strong(text)
                if not is_strong:
                    await event.respond(
                        f"Пароль не соответствует требованиям: {message} Пожалуйста, повторите ввод пароля:")
                    return

                new_hashed_password = hash_password(text)
                user_bot = session.query(UserBot).filter_by(id=user_id).first()
                user_bot.pass_hash = new_hashed_password
                session.commit()

                del change_password_state[user_id]
                password_required_after_menu[user_id] = False

                await event.respond(get_text(language, 'password_changed'),
                                    buttons=create_back_to_main_menu_keyboard(language))
                await event.delete()
                # change_password_state[user_id] = "Done"


        elif user_id in activate_premium_state:
            if activate_premium_state[user_id] == "waiting_for_premium_key":
                with open('keys.txt', 'r') as f:
                    keys = [line.strip() for line in f]

                if text in keys:
                    user_bot = session.query(UserBot).filter_by(id=user_id).first()
                    premium_expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
                    user_bot.premium = premium_expiration_date
                    session.commit()

                    keys.remove(text)
                    with open('keys.txt', 'w') as f:
                        for key in keys:
                            f.write(key + '\n')

                    del activate_premium_state[user_id]

                    await event.respond(get_text(language, 'premium_activated_message'),
                                        buttons=create_back_to_main_menu_keyboard(language))
                else:
                    # Сообщаем пользователю, что ключ недействителен, на его языке
                    await event.respond(get_text(language, 'invalid_premium_key'),
                                        buttons=create_back_to_main_menu_keyboard(language))

        elif user_id in module_creation_state:
            if module_creation_state[user_id]["state"] == "waiting_for_module_name":
                module_creation_state[user_id]["name"] = text
                module_creation_state[user_id]["state"] = "waiting_for_module_description"

                # Предлагаем ввести описание модуля или пропустить этот шаг
                await event.respond(get_text(language, 'enter_module_description'),
                                    buttons=[
                                        [Button.inline(get_text(language, 'skip_description'),
                                                       data=b"skip_description")]])

            elif module_creation_state[user_id]["state"] == "waiting_for_module_description":
                if len(text) <= 100:
                    module_creation_state[user_id]["description"] = text

                    # Создаем модуль в базе данных
                    new_module = Collection(
                        id=generate_unique_module_id(),  # Генерация случайного ID
                        owner=user_id,
                        name=module_creation_state[user_id]["name"],
                        descript=module_creation_state[user_id]["description"],
                        lang1=module_creation_state[user_id]["lang1"],
                        lang2=module_creation_state[user_id]["lang2"]
                    )
                    session.add(new_module)
                    session.commit()

                    module_id = new_module.id  # Получаем ID созданного модуля

                    # Очищаем состояние создания модуля
                    del module_creation_state[user_id]

                    # Предлагаем добавить карточки в модуль
                    await event.respond(get_text(language, 'module_created_add_cards'),
                                        buttons=create_add_cards_keyboard(language))

                    # Инициализируем состояние создания карточек для этого модуля
                    card_creation_state[user_id] = {"state": "idle", "module_id": module_id}
                else:
                    # Сообщаем, что описание слишком длинное
                    await event.respond(get_text(language, 'description_too_long'))

        elif user_id in card_creation_state:
            if card_creation_state[user_id]["state"] == "waiting_for_foreign_word":
                foreign_word = text[:100]  # Обрезаем до 100 символов
                card_creation_state[user_id]["foreign_word"] = foreign_word
                card_creation_state[user_id]["state"] = "waiting_for_translation"
                await event.respond(get_text(language, 'enter_translation'))

            elif card_creation_state[user_id]["state"] == "waiting_for_translation":
                translation = text[:100]  # Обрезаем до 100 символов
                card_creation_state[user_id]["translation"] = translation
                card_creation_state[user_id]["state"] = "waiting_for_image_choice"
                await event.respond(get_text(language, 'add_image_to_card'),
                                    buttons=create_add_image_keyboard(language))

        # Обработка ввода названия модуля для поиска
        elif user_id in module_view_state and module_view_state[user_id]['state'] == 'waiting_for_module_name':
            search_term = text.strip().lower()
            modules = session.query(Collection).filter(
                Collection.name.like(f"%{search_term}%")
            ).all()

            if modules:
                module_buttons = [[Button.inline(module.name, data=f"view_module_{module.id}")] for module in
                                  modules]
                module_buttons.append(create_back_to_main_menu_keyboard(language)[0])
                await event.respond(get_text(language, 'modules_found'), buttons=module_buttons)
            else:
                await event.respond(get_text(language, 'no_modules_found'),
                                    buttons=create_back_to_main_menu_keyboard(language))

            # Очищаем состояние
            del module_view_state[user_id]
        session.close()

    async def send_main_menu_new_message(event):  # Новая функция для отправки нового сообщения
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        await client.send_file(event.chat_id, MAIN_MENU_IMG_PATH, caption=get_text(language, 'main_menu'),
                               buttons=create_main_menu_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(data=b"skip_description"))
    async def skip_description_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        if user_id in module_creation_state and module_creation_state[user_id][
            "state"] == "waiting_for_module_description":
            # Создаем модуль в базе данных с пустым описанием
            new_module = Collection(
                id=generate_unique_module_id(),  # Генерация случайного ID
                owner=user_id,
                name=module_creation_state[user_id]["name"],
                descript="",  # Пустое описание
                lang1=module_creation_state[user_id]["lang1"],
                lang2=module_creation_state[user_id]["lang2"]
            )
            session.add(new_module)
            session.commit()

            module_id = new_module.id  # Получаем ID созданного модуля

            # Очищаем состояние создания модуля
            del module_creation_state[user_id]

            # Предлагаем добавить карточки в модуль
            await event.respond(get_text(language, 'module_created_add_cards'),
                                buttons=create_add_cards_keyboard(language))

            # Инициализируем состояние создания карточек для этого модуля
            card_creation_state[user_id] = {"state": "idle", "module_id": module_id}
        session.close()

    @client.on(events.CallbackQuery(data=b"change_nickname"))
    async def change_nickname_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        user_bot = session.query(UserBot).filter_by(id=user_id).first()
        if not user_bot:
            await event.answer("Пожалуйста, зарегистрируйтесь, прежде чем использовать эту функцию.")
            return

        nickname = user_bot.nick
        change_nickname_state[user_id] = "waiting_for_new_nickname"
        await event.respond(get_text(language, 'enter_new_nickname', nickname),
                            buttons=create_back_to_main_menu_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(data=b"change_password"))
    async def change_password_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        change_password_state[user_id] = "waiting_for_old_password"
        await event.respond(get_text(language, 'enter_old_password'),
                            buttons=create_back_to_main_menu_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(data=b"activate_premium"))
    async def activate_premium_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        activate_premium_state[user_id] = "waiting_for_premium_key"
        await event.respond(get_text(language, 'enter_premium_key'),
                            buttons=create_back_to_main_menu_keyboard(language))
        session.close()

    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        session = Session()
        user_id = event.sender_id
        username = event.sender.username or "NO_USERNAME"

        user_tg = session.query(UserTg).filter_by(id=user_id).first()

        if not user_tg:
            new_user_tg = UserTg(id=user_id, username=username, date=datetime.datetime.now())
            session.add(new_user_tg)
            session.commit()
            print(f"Новый пользователь Telegram добавлен: {user_id}, @{username}")
            await event.respond(get_text('ru', 'start_message'), buttons=create_language_selection_keyboard())
        else:
            language = user_tg.language
            user_bot = session.query(UserBot).filter_by(id=user_id).first()
            if user_bot:
                if user_id in password_required_after_menu and password_required_after_menu[user_id]:
                    await event.respond(get_text(language, 'enter_new_password'))
                else:
                    await send_main_menu_new_message(event)
            else:
                await event.respond(get_text(language, 'register_message'),
                                    buttons=[[Button.inline(get_text(language, 'register'), data=b"Register")]])
        session.close()

    @client.on(events.CallbackQuery(data=b"Register"))
    async def registration_button(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'
        registration_state[user_id] = "waiting_for_nickname"
        await event.respond(get_text(language, 'nickname_request'))
        session.close()

    @client.on(events.CallbackQuery(data=b"skip_image"))
    async def skip_image_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        if user_id in card_creation_state and card_creation_state[user_id]["state"] == "waiting_for_image_choice":
            # Получаем данные из состояния
            module_id = card_creation_state[user_id]["module_id"]
            foreign_word = card_creation_state[user_id]["foreign_word"]
            translation = card_creation_state[user_id]["translation"]

            # Получаем последний ID из базы данных и увеличиваем на 1
            last_card = session.query(Card).order_by(Card.id.desc()).first()
            new_card_id = last_card.id + 1 if last_card else 1

            # Создаем новую карточку в базе данных
            new_card = Card(
                id=new_card_id,
                name=foreign_word,
                translation=translation,
                collection=module_id,
                image_path=None  # Изображение пропускаем
            )
            session.add(new_card)
            session.commit()

            # Очищаем данные для текущей карточки
            card_creation_state[user_id]["state"] = "idle"
            del card_creation_state[user_id]["foreign_word"]
            del card_creation_state[user_id]["translation"]

            # Отправляем сообщение об успешном сохранении и предлагаем добавить следующую
            await client.edit_message(event.chat_id, event.message_id, get_text(language, 'card_saved_add_next'),
                                      buttons=create_card_saved_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(data=b"add_image"))
    async def add_image_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        if user_id in card_creation_state and card_creation_state[user_id]["state"] == "waiting_for_image_choice":
            # Переходим в состояние ожидания изображения
            card_creation_state[user_id]["state"] = "waiting_for_image"
            await client.edit_message(event.chat_id, event.message_id,
                                      "Пожалуйста, отправьте изображение для карточки.")
        session.close()

    @client.on(events.NewMessage(pattern=None, func=lambda e: e.photo or e.document))
    async def image_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        if user_id in card_creation_state and card_creation_state[user_id]["state"] == "waiting_for_image":
            try:
                # Получаем данные из состояния
                module_id = card_creation_state[user_id]["module_id"]
                foreign_word = card_creation_state[user_id]["foreign_word"]
                translation = card_creation_state[user_id]["translation"]

                # Получаем последний ID из базы данных и увеличиваем на 1
                last_card = session.query(Card).order_by(Card.id.desc()).first()
                new_card_id = last_card.id + 1 if last_card else 1
                # Отправляем сообщение об успешном сохранении и предлагаем добавить следующую карточку
                await client.send_message(event.chat_id, get_text(language, 'card_saved_add_next'),
                                          buttons=create_card_saved_keyboard(language))

                # Получаем информацию о файле
                if event.photo:
                    image_data = await event.download_media(bytes)
                    file_name = f"{new_card_id}.jpg"
                elif event.document:
                    if event.document.mime_type not in ['image/jpeg', 'image/png']:
                        await event.respond(get_text(language, 'invalid_image_format'))
                        return

                    image_data = await event.download_media(bytes)
                    file_name = f"{new_card_id}.jpg"

                # Создаем папку для модуля, если ее нет
                module_folder = os.path.join(CARDS_FOLDER, str(module_id))
                if not os.path.exists(module_folder):
                    os.makedirs(module_folder)

                # Сохраняем изображение в формате JPEG
                image_path = os.path.join(module_folder, file_name)
                image = Image.open(io.BytesIO(image_data))
                image = image.convert("RGB")  # Преобразуем в RGB, если изображение в другом формате
                image.save(image_path, "JPEG")

                # Создаем новую карточку в базе данных
                new_card = Card(
                    id=new_card_id,
                    name=foreign_word,
                    translation=translation,
                    collection=module_id,
                    image_path=image_path  # Сохраняем путь к изображению
                )
                session.add(new_card)
                session.commit()

                # Очищаем данные для текущей карточки
                card_creation_state[user_id]["state"] = "idle"
                del card_creation_state[user_id]["foreign_word"]
                del card_creation_state[user_id]["translation"]

                # Отправляем сообщение об успешном сохранении и предлагаем добавить следующую
                await client.edit_message(event.chat_id, event.message_id,
                                          get_text(language, 'card_saved_add_next'),
                                          buttons=create_card_saved_keyboard(language))

            except Exception as e:
                1 + 1
        session.close()

    @client.on(events.CallbackQuery(data=b"add_next_card_action"))  # Изменено data
    async def add_next_card_action_handler(event):  # Переименовано название функции
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        if user_id in card_creation_state:
            # Устанавливаем состояние ожидания ввода иностранного слова
            card_creation_state[user_id]["state"] = "waiting_for_foreign_word"
            await client.send_message(event.chat_id,
                                      get_text(language, 'enter_foreign_word'))  # Отправляем новое сообщение
        session.close()

    # Обработчики для просмотра модулей и карточек
    @client.on(events.CallbackQuery(data=b"my_modules"))
    async def my_modules_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        modules = session.query(Collection).filter_by(owner=user_id).all()

        if modules:
            module_buttons = [[Button.inline(module.name, data=f"view_module_{module.id}")] for module in modules]
            module_buttons.append(create_back_to_main_menu_keyboard(language)[0])
            await client.edit_message(event.chat_id, event.message_id, "Ваши модули:", buttons=module_buttons)
        else:
            await client.edit_message(event.chat_id, event.message_id,
                                      "😯 У вас пока нет модулей.\n\nНо вы всегда можете добавить новые, выйдя в главное меню!",
                                      buttons=create_back_to_main_menu_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(data=b"other_modules"))
    async def other_modules_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        # Устанавливаем состояние ожидания ввода названия модуля
        module_view_state[user_id] = {'state': 'waiting_for_module_name'}
        await client.edit_message(event.chat_id, event.message_id, get_text(language, 'module_name_request'),
                                  buttons=create_back_to_main_menu_keyboard(language))
        session.close()

    @client.on(events.CallbackQuery(pattern=r"view_module_(\d+)"))
    async def view_module_handler(event):
        session = Session()
        user_id = event.sender_id
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        module_id = int(event.data.decode('utf-8').split('_')[2])
        module = session.query(Collection).filter_by(id=module_id).first()

        if not module:
            await event.answer("Модуль не найден.")
            return

        cards = session.query(Card).filter_by(collection=module_id).all()

        if not cards:
            await client.edit_message(event.chat_id, event.message_id, get_text(language, 'no_cards_in_module'),
                                      buttons=create_back_to_main_menu_keyboard(language))
            return

        # Инициализируем состояние просмотра карточек
        module_view_state[user_id] = {
            'module_id': module_id,
            'cards': cards,
            'current_card_index': 0,
            'card_face': 'front',  # 'front' или 'back'
            'message_id': None  # Добавляем поле для хранения ID сообщения с карточкой
        }

        await show_card(event, user_id)
        session.close()

    async def show_card(event, user_id):
        session = Session()
        user_tg = session.query(UserTg).filter_by(id=user_id).first()
        language = user_tg.language if user_tg else 'ru'

        state = module_view_state[user_id]
        module_id = state['module_id']
        cards = state['cards']
        current_card_index = state['current_card_index']
        card_face = state['card_face']
        message_id = state['message_id']

        if current_card_index >= len(cards):
            # Если все карточки пройдены, удаляем текущее сообщение и выводим сообщение об окончании
            if message_id:
                try:
                    await client.delete_messages(event.chat_id, message_id)
                except Exception as e:
                    print(f"Ошибка при удалении сообщения: {e}")

            await client.send_message(event.chat_id, get_text(language, 'all_cards_passed'),
                                      buttons=create_back_to_main_menu_keyboard(
                                          language))  # Отправляем новое сообщение
            del module_view_state[user_id]
            return

        card = cards[current_card_index]

        # Формируем сообщение и клавиатуру
        if card_face == 'front':
            text = get_text(language, 'card_front', card.name)
        else:
            text = get_text(language, 'card_back', card.translation)

        keyboard = create_module_keyboard(language, module_id)

        # Отправляем или редактируем сообщение с карточкой
        try:
            image_path = card.image_path if card.image_path else NON_IMAGE_PATH
            if message_id:
                # Редактируем старое сообщение
                await client.edit_message(event.chat_id, message_id, text, buttons=keyboard, file=image_path)
            else:
                # Отправляем новое сообщение и сохраняем его ID
                sent_message = await client.send_file(event.chat_id, image_path, caption=text, buttons=keyboard)
                module_view_state[user_id]['message_id'] = sent_message.id

        except Exception as e:
            print(f"Ошибка при отправке/редактировании карточки: {e}")
            await event.respond(text,
                                buttons=keyboard)  # Отправляем только текст, если не удалось отправить изображение
        session.close()

    @client.on(events.CallbackQuery(pattern=r"flip_(\d+)"))
    async def flip_card_handler(event):
        user_id = event.sender_id

        if user_id in module_view_state:
            state = module_view_state[user_id]
            if state['card_face'] == 'front':
                state['card_face'] = 'back'
            else:
                state['card_face'] = 'front'
            await show_card(event, user_id)

    @client.on(events.CallbackQuery(pattern=r"next_(\d+)"))
    async def next_card_handler(event):
        user_id = event.sender_id

        if user_id in module_view_state:
            state = module_view_state[user_id]
            state['current_card_index'] += 1
            state['card_face'] = 'front'  # Сбрасываем на лицевую сторону
            await show_card(event, user_id)
