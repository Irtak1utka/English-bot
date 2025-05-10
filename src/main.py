import asyncio
import hashlib
import os
import random
import io
from telethon import TelegramClient, events, Button
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime
from PIL import Image

from SECRETS import API_ID, API_HASH, BOT_TOKEN

DATABASE_URL = "sqlite:///" + os.path.abspath("db.sqlite")
CARDS_FOLDER = "cards_folder"
USUAL_IMG_FOLDER = os.path.join(CARDS_FOLDER, "usual_img")
NON_IMAGE_PATH = os.path.join(USUAL_IMG_FOLDER, "non_image.png")
MAIN_MENU_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "main_menu.png")
STARS_LEARN_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "stars_learn.png")
CREATE_NEW_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "create_new.png")
INFO_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "info.png")
HOW_TO_USE_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "how_to_use.png")
MY_ACC_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "my_acc.png")

if not os.path.exists(CARDS_FOLDER):
    os.makedirs(CARDS_FOLDER)
if not os.path.exists(USUAL_IMG_FOLDER):
    os.makedirs(USUAL_IMG_FOLDER)
    if not os.path.exists(NON_IMAGE_PATH):
        Image.new('RGB', (100, 100), 'white').save(NON_IMAGE_PATH)
    if not os.path.exists(MAIN_MENU_IMG_PATH):
        Image.new('RGB', (100, 100), 'white').save(MAIN_MENU_IMG_PATH)
    if not os.path.exists(STARS_LEARN_IMG_PATH):
        Image.new('RGB', (100, 100), 'white').save(STARS_LEARN_IMG_PATH)
    if not os.path.exists(CREATE_NEW_IMG_PATH):
        Image.new('RGB', (100, 100), 'white').save(CREATE_NEW_IMG_PATH)
    if not os.path.exists(INFO_IMG_PATH):
        Image.new('RGB', (100, 100), 'white').save(INFO_IMG_PATH)
    if not os.path.exists(HOW_TO_USE_IMG_PATH):
        Image.new('RGB', (100, 100), 'white').save(HOW_TO_USE_IMG_PATH)
    if not os.path.exists(MY_ACC_IMG_PATH):
        Image.new('RGB', (100, 100), 'white').save(MY_ACC_IMG_PATH)

Base = declarative_base()


class UserTg(Base):
    __tablename__ = "users_tg"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    admin = Column(Integer, default=0)
    ban = Column(Integer, default=0)
    language = Column(String, default='ru')
    date = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<UserTg(id={self.id}, username='{self.username}', admin={self.admin}, ban={self.ban}, language='{self.language}', date='{self.date}')>"


class UserBot(Base):
    __tablename__ = "users_bot"

    id = Column(Integer, primary_key=True)
    nick = Column(String, unique=True)
    pass_hash = Column(String)
    count_of_cards = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    premium = Column(DateTime)

    def __repr__(self):
        return f"<UserBot(id={self.id}, nick='{self.nick}', count_of_cards={self.count_of_cards}, rank={self.rank}, premium={self.premium})>"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    translation = Column(String)
    collection = Column(Integer, ForeignKey('collection.id'))
    collection_rel = relationship("Collection", back_populates="cards")
    image_path = Column(String, nullable=True)  # Добавляем поле для хранения пути к изображению

    def __repr__(self):
        return f"<Card(id={self.id}, name='{self.name}', translation='{self.translation}', collection={self.collection})>"


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True)
    owner = Column(Integer)  # Добавлено поле owner
    name = Column(String)
    descript = Column(String)
    lang1 = Column(String)  # Язык оригинала
    lang2 = Column(String)  # Язык перевода
    cards = relationship("Card", back_populates="collection_rel")

    def __repr__(self):
        return f"<Collection(id={self.id}, owner={self.owner}, name='{self.name}', descript='{self.descript}, lang1='{self.lang1}, lang2='{self.lang2}')>"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    id_to = Column(Integer)
    id_from = Column(Integer)
    review = Column(String)
    score = Column(Integer)

    def __repr__(self):
        return f"<Review(id={self.id}, id_to={self.id_to}, id_from={self.id_from}, score={self.score})>"


engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
print("База данных успешно создана!")

Session = sessionmaker(bind=engine)
session = Session()

client = TelegramClient('session_name', API_ID, API_HASH)


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


def is_password_strong(password):
    if len(password) < 5:
        return False, "Пароль должен содержать не менее 5 символов."
    if not any(char.isdigit() for char in password):
        return False, "Пароль должен содержать хотя бы одну цифру."
    if not any(char.isalpha() for char in password):
        return False, "Пароль должен содержать хотя бы одну букву."
    if not any(not char.isalnum() for char in password):
        return False, "Пароль должен содержать хотя бы один специальный символ."
    return True, None


texts = {
    'ru': {
        'start_message': "Привет! Выберите язык интерфейса бота:",
        'register_message': "Отлично, продолжим на русском языке!\n\n Похоже, ты еще не зарегистрирован. Нажми кнопку ниже, чтобы зарегистрироваться.",
        'nickname_request': "Пожалуйста, введи никнейм для регистрации:",
        'nickname_taken': "Этот никнейм уже занят. Пожалуйста, выберите другой:",
        'password_request': "👌 Давай обезопасим твой профиль. Введи пароль:",
        'registration_complete': "Регистрация завершена!",
        'main_menu': "😯✨ Ты попал в главное меню бота!\n \n- Здесь ты можешь создать модуль для изучения новых слов, проверить свои знания с помощью тренировок и многое другое!\n\nВыберите нужную вам опцию в меню, чтобы начать работу с ботом.",
        'start_learning': "✔ Начать обучение",
        'create_module': "✔ Создать новый модуль",
        'bot_info': "ℹ Информация о боте",
        'how_to_use': "😦 Как пользоваться ботом",
        'my_account': "👀 Мой аккаунт",
        'back_to_main_menu': "⬅ Вернуться в главное меню",
        'my_account_info': "Ваш id - {}\n"
                           "----------------------\n"
                           "Никнейм - {}\n"
                           "Дата регистрации - {}\n"
                           "Количество созданных карточек - {}\n"
                           "-------------------------\n"
                           "Рейтинг - {}\n"
                           "Премиум активен до: {}",
        'how_to_use_info': "- В нашем боте есть много функций, которые помогут тебе эффективно изучать иностранный язык.\n\n🤞 Начнем с создания новых модулей обучения. Для этого выберите соответствующую опцию в меню и следуйте инструкциям на экране. После создания модуля ты сможешь поделиться им с друзьями и продолжить обучение вместе!\n\n- Для проверки своих знаний вы можно использовать как свою личные модули, так и чужие. Вернитесь в главное меню и нажмите на кнопку 'НАЧАТЬ ОБУЧЕНИЕ'.\n\n✨ Зайдя во вкладку 'МОЙ АККАУНТ', вы сможете обеспечить его безопасность, получить и активировать премиум доступ к боту на 1 месяц, изменить язык интерфейса, что тоже отлично поможет в изучении иностранной лексики! ",
        'support': "Поддержка",
        'start_learning_message': "⏱ Очень рад, что у тебя появилось желание изучить новые иностранные слова!\n\nВыбери нужную опцию, нажав на кнопку ниже.",
        'my_modules': "Посмотреть свои модули",
        'other_modules': "Посмотреть чужие модули",
        'edit_modules_message': "тут что то написано, якобы инструкция",
        'create_module': "Создать новый модуль",
        'edit_existing_module': "Редактировать имеющийся модуль",
        'bot_info_message': "ℹ Проект PUZLE ENGLISH LEANING был создан в 2025 году для помощи в изучении иностранных слов!\n\nЕдиная цель проекта - максимально эффективное и комфортное изучение иностранного языка прямо в мессенджере Telegram. Это не просто умная система, это ваш личный помощник в пути к совершенству!",
        'change_language': "Сменить язык",
        'register': "Зарегистрироваться",
        'change_nickname': "Сменить ник",
        'change_password': "Сменить пароль",
        'get_premium': "Получить премиум",
        'activate_premium': "Активировать премиум",
        'enter_new_nickname': "Введите никнейм, на который Вы хотите изменить свой нынешний ник - {}",
        'nickname_exists': "Подобный ник уже существует, пожалуйста введите другой никнейм",
        'enter_old_password': "Введите прошлый пароль, для подтверждения личности",
        'incorrect_password': "Неверный пароль, попробуйте еще раз",
        'enter_new_password': "Введите новый пароль",
        'premium_link': "https://t.me/telegram",
        'enter_premium_key': "Введите ключ, на активации доступа",
        'invalid_premium_key': "❌ Не верный ключ, попробуйте еще раз",
        'nickname_changed': "Никнейм успешно изменен",
        'password_changed': "Пароль успешно изменен",
        'premium_activated': "Премиум успешно активирован до {}",
        'premium_activated_message': "Доступ на 1 месяц активирован",
        'select_original_language': "👀 Отлично, давай созданим новый модуль!\n\nВыберите язык, на котором будут записаны иностранные слова",
        'select_translation_language': "✔ А теперь выберите язык, на который будут переведены иностранные слова",
        'enter_module_name': "🔥 Давай придумаем название для нового модуля!\n\nСоветуем избегать коротких названий, так вы не сможете передать общую тему слов, которые запишете в данном модуле. ",
        'enter_module_description': "При необходимости укажите описание для нового модуля",
        'skip_description': "Пропустить",
        'description_too_long': "Описание должно быть не более 100 символов. Пожалуйста, попробуйте еще раз.",
        'module_created_add_cards': "Отлично, новый модуль создан, добавим в него карточек с новыми словами для изучения?",
        'add_cards': "💹 Добавим карточки",
        'enter_foreign_word': "Введите слово на иностранном языке (максимум 100 символов):",
        'enter_translation': "Введите перевод слова (максимум 100 символов):",
        'add_image_to_card': "Добавим к этой карточке картинку?",
        'skip': "Пропустить",
        'add': "Добавим!",
        'card_saved_add_next': "Карточка успешно сохранена, добавим следующую или вернемся в главное меню?",
        'add_next_card': "Добавить следующую карточку",
        'invalid_image_format': "Неверный формат изображения. Пожалуйста, отправьте изображение в формате JPEG или PNG.",
        'module_name_request': "Введите название модуля для поиска:",
        'no_modules_found': "Модулей с подобным названием найдено не было.",
        'modules_found': "Вот найденные модули:",
        'no_cards_in_module': "В этом модуле пока нет карточек.",
        'card_front': "{}",  # Текст для лицевой стороны карточки (иностранное слово)
        'card_back': "{}",  # Текст для обратной стороны карточки (перевод)
        'flip': "Перевернуть",
        'next': "Далее",
        'all_cards_passed': "Вы прошли все карточки!",
    },
    'en': {
        'start_message': "Hello! Choose a language:",
        'register_message': "Hello! It seems you are not registered yet. Click the button below to register.",
        'nickname_request': "Please enter your nickname:",
        'nickname_taken': "This nickname is already taken. Please choose another:",
        'password_request': "Now enter your password:",
        'registration_complete': "Registration complete!",
        'main_menu': "Main Menu",
        'start_learning': "✔ Start Learning",
        'create_module': "✔ Create New Module",
        'bot_info': "ℹ Bot Info",
        'how_to_use': "😦 How to Use Bot",
        'my_account': "👀 My Account",
        'back_to_main_menu': "⬅ Back to Main Menu",
        'my_account_info': "Your id - {}\n"
                           "----------------------\n"
                           "Nickname - {}\n"
                           "Registration date - {}\n"
                           "Number of created cards - {}\n"
                           "-------------------------\n"
                           "Rating - {}\n"
                           "Premium active until: {}",
        'how_to_use_info': "Here's how to use it",
        'support': "Support",
        'start_learning_message': "Great, let's start",
        'my_modules': "View My Modules",
        'other_modules': "View Other Modules",
        'edit_modules_message': "some instructions here",
        'create_module': "Create New Module",
        'edit_existing_module': "Edit Existing Module",
        'bot_info_message': "Here is info",
        'change_language': "Change language",
        'register': "Register",
        'change_nickname': "Change nickname",
        'change_password': "Change password",
        'get_premium': "Get premium",
        'activate_premium': "Activate premium",
        'enter_new_nickname': "Enter the nickname you want to change your current nickname to - {}",
        'nickname_exists': "This nickname already exists, please enter another nickname",
        'enter_old_password': "Enter your old password to confirm your identity",
        'incorrect_password': "Incorrect password, please try again",
        'enter_new_password': "Enter a new password",
        'premium_link': "https://t.me/telegram",
        'enter_premium_key': "Enter the activation key",
        'invalid_premium_key': "❌ Invalid key, please try again",
        'nickname_changed': "Nickname changed successfully",
        'password_changed': "Password changed successfully",
        'premium_activated': "Premium activated successfully until {}",
        'premium_activated_message': "Access for 1 month activated",
        'select_original_language': "Select the language in which the foreign words will be written",
        'select_translation_language': "Select the language into which the words in the module will be translated",
        'enter_module_name': "Enter a name for the module",
        'enter_module_description': "If necessary, enter a description for the new module",
        'skip_description': "Skip",
        'description_too_long': "The description must be no more than 100 characters. Please try again.",
        'module_created_add_cards': "Great, the new module has been created. Do you want to add cards with new words to study?",
        'add_cards': "💹 Add cards",
        'enter_foreign_word': "Enter a word in a foreign language (maximum 100 characters):",
        'enter_translation': "Enter the translation of the word (maximum 100 characters):",
        'add_image_to_card': "Add an image to this card?",
        'skip': "Skip",
        'add': "Add!",
        'card_saved_add_next': "The card has been successfully saved. Add the next one or return to the main menu?",
        'add_next_card': "Add the next card",
        'invalid_image_format': "Invalid image format. Please send an image in JPEG or PNG format.",
        'module_name_request': "Enter the module name to search:",
        'no_modules_found': "No modules with a similar name were found.",
        'modules_found': "Here are the modules found:",
        'no_cards_in_module': "There are no cards in this module yet.",
        'card_front': "{}",  # Текст для лицевой стороны карточки (иностранное слово)
        'card_back': "{}",  # Текст для обратной стороны карточки (перевод)
        'flip': "Flip",
        'next': "Next",
        'all_cards_passed': "You have passed all the cards!",
    },
    'uk': {
        'start_message': "Привіт! Оберіть мову:",
        'register_message': "Привіт! Схоже, ви ще не зареєстровані. Натисніть кнопку нижче, щоб зареєструватися.",
        'nickname_request': "Будь ласка, введіть свій нікнейм:",
        'nickname_taken': "Це ім'я користувача вже зайнято. Будь ласка, оберіть інше:",
        'password_request': "Тепер введіть свій пароль:",
        'registration_complete': "Реєстрація завершена!",
        'main_menu': "Головне меню",
        'start_learning': "✔ Розпочати навчання",
        'create_module': "✔ Створити новий модуль",
        'bot_info': "ℹ Інформація про бота",
        'how_to_use': "😦 Як користуватися ботом",
        'my_account': "👀 Мій аккаунт",
        'back_to_main_menu': "⬅ Повернутися до головного меню",
        'my_account_info': "Ваш id - {}\n"
                           "----------------------\n"
                           "Нікнейм - {}\n"
                           "Дата реєстрації - {}\n"
                           "Кількість створених карток - {}\n"
                           "-------------------------\n"
                           "Рейтинг - {}\n"
                           "Преміум активний до: {}",
        'how_to_use_info': "Користуватися потрібно ось так",
        'support': "Підтримка",
        'start_learning_message': "Чудово, почнімо",
        'my_modules': "Переглянути мої модулі",
        'other_modules': "Переглянути інші модулі",
        'edit_modules_message': "тут щось написано, нібито інструкція",
        'create_module': "Створити новий модуль",
        'edit_existing_module': "Редагувати існуючий модуль",
        'bot_info_message': "Тут інформація",
        'change_language': "Змінити мову",
        'register': "Зареєструватися",
        'change_nickname': "Змінити нік",
        'change_password': "Змінити пароль",
        'get_premium': "Отримати преміум",
        'activate_premium': "Активувати преміум",
        'enter_new_nickname': "Введіть нікнейм, на який Ви хочете змінити свій поточний нік - {}",
        'nickname_exists': "Подібний нік вже існує, будь ласка, введіть інший нікнейм",
        'enter_old_password': "Введіть минулий пароль, для підтвердження особистості",
        'incorrect_password': "Невірний пароль, спробуйте ще раз",
        'enter_new_password': "Введіть новий пароль",
        'premium_link': "https://t.me/telegram",
        'enter_premium_key': "Введіть ключ, на активації доступу",
        'invalid_premium_key': "❌ Невірний ключ, спробуйте ще раз",
        'nickname_changed': "Нікнейм успішно змінено",
        'password_changed': "Пароль успішно змінено",
        'premium_activated': "Преміум успішно активовано до {}",
        'premium_activated_message': "Доступ на 1 місяць активовано",
        'select_original_language': "Виберіть мову, на якій будуть записані іноземні слова",
        'select_translation_language': "Виберіть мову, на яку будуть перекладені слова в модулі",
        'enter_module_name': "Введіть назву для модуля",
        'enter_module_description': "За потреби вкажіть опис для нового модуля",
        'skip_description': "Пропустити",
        'description_too_long': "Опис має бути не більше 100 символів. Будь ласка, спробуйте ще раз.",
        'module_created_add_cards': "Чудово, новий модуль створено, чи хочете додати картки для вивчення?",
        'add_cards': "💹 Додати картки",
        'enter_foreign_word': "Введіть слово іноземною мовою (максимум 100 символів):",
        'enter_translation': "Введіть переклад слова (максимум 100 символів):",
        'add_image_to_card': "Додати зображення до картки?",
        'skip': "Пропустити",
        'add': "Додати!",
        'card_saved_add_next': "Картка успішно збережена, додати ще чи повернутися до головного меню?",
        'add_next_card': "Додати наступну картку",
        'invalid_image_format': "Невірний формат зображення. Будь ласка, надішліть зображення у форматі JPEG або PNG.",
        'module_name_request': "Введіть назву модуля для пошуку:",
        'no_modules_found': "Модулів з подібною назвою не було знайдено.",
        'modules_found': "Ось знайдені модулі:",
        'no_cards_in_module': "У цьому модулі поки немає карток.",
        'card_front': "{}",  # Текст для лицевой стороны карточки (иностранное слово)
        'card_back': "{}",  # Текст для зворотної сторони картки (переклад)
        'flip': "Перевернути",
        'next': "Далі",
        'all_cards_passed': "Ви пройшли всі картки!",
    },
    'pl': {
        'start_message': "Cześć! Wybierz język:",
        'register_message': "Cześć! Wygląda na to, że nie jesteś jeszcze zarejestrowany. Kliknij przycisk poniżej, aby się zarejestrować.",
        'nickname_request': "Proszę wprowadzić swój pseudonim:",
        'nickname_taken': "Ta nazwa użytkownika jest już zajęta. Proszę wybrać inną:",
        'password_request': "Teraz wprowadź swoje hasło:",
        'registration_complete': "Rejestracja zakończona!",
        'main_menu': "Menu główne",
        'start_learning': "✔ Rozpocznij naukę",
        'create_module': "✔ Utwórz nowy moduł",
        'bot_info': "ℹ Informacje o bocie",
        'how_to_use': "😦 Jak korzystać z bota",
        'my_account': "👀 Moje konto",
        'back_to_main_menu': "⬅ Powrót do menu głównego",
        'my_account_info': "Twój id - {}\n"
                           "----------------------\n"
                           "Pseudonim - {}\n"
                           "Data rejestracji - {}\n"
                           "Liczba utworzonych kart - {}\n"
                           "-------------------------\n"
                           "Ocena - {}\n"
                           "Premium aktywne do: {}",
        'how_to_use_info': "Aby z niego korzystać, zrób tak",
        'support': "Wsparcie",
        'start_learning_message': "Świetnie, zacznijmy",
        'my_modules': "Wyświetl moje moduły",
        'other_modules': "Wyświetl inne moduły",
        'edit_modules_message': "tutaj coś jest napisane, rzekomo instrukcja",
        'create_module': "Utwórz nowy moduł",
        'edit_existing_module': "Edytuj istniejący moduł",
        'bot_info_message': "Tutaj informacje",
        'change_language': "Zmień język",
        'register': "Zarejestruj się",
        'change_nickname': "Zmień pseudonim",
        'change_password': "Zmień hasło",
        'get_premium': "Zdobądź premium",
        'activate_premium': "Aktywuj premium",
        'enter_new_nickname': "Wprowadź pseudonim, na który chcesz zmienić swój obecny pseudonim - {}",
        'nickname_exists': "Ta nazwa użytkownika już istnieje, wprowadź inną nazwę użytkownika",
        'enter_old_password': "Wprowadź stare hasło, aby potwierdzić swoją tożsamość",
        'incorrect_password': "Nieprawidłowe hasło, spróbuj ponownie",
        'enter_new_password': "Wprowadź nowe hasło",
        'premium_link': "https://t.me/telegram",
        'enter_premium_key': "Wprowadź klucz aktywacyjny",
        'invalid_premium_key': "❌ Nieprawidłowy klucz, spróbuj ponownie",
        'nickname_changed': "Pseudonim został pomyślnie zmieniony",
        'password_changed': "Hasło zostało pomyślnie zmienione",
        'premium_activated': "Premium aktywowane pomyślnie do {}",
        'premium_activated_message': "Dostęp na 1 miesiąц aktywowano",
        'select_original_language': "Wybierz język, w którym zostaną zapisane słowa obce",
        'select_translation_language': "Wybierz język, na który zostaną przetłumaczone słowa w module",
        'enter_module_name': "Wprowadź nazwę modułu",
        'enter_module_description': "W razie potrzeby wprowadź opis nowego modułu",
        'skip_description': "Pominąć",
        'description_too_long': "Opis musi mieć nie więcej niż 100 znaków. Proszę spróbuj ponownie.",
        'module_created_add_cards': "Świetnie, nowy moduł został utworzony, chcesz dodać karty do nauki?",
        'add_cards': "💹 Dodaj kartki",
        'enter_foreign_word': "Wprowadź słowo w języku obcym (maksymalnie 100 znaków):",
        'enter_translation': "Wprowadź tłumaczenie słowa (maksymalnie 100 znaków):",
        'add_image_to_card': "Dodać obrazek do karty?",
        'skip': "Pominąć",
        'add': "Dodaj!",
        'card_saved_add_next': "Karta została zapisana, dodać następną czy wrócić do menu głównego?",
        'add_next_card': "Dodaj następną kartę",
        'invalid_image_format': "Nieprawidłowy format obrazu. Proszę wysłać obraz w formacie JPEG lub PNG.",
        'module_name_request': "Wprowadź nazwę modułu do wyszukania:",
        'no_modules_found': "Nie znaleziono modułów o podobnej nazwie.",
        'modules_found': "Oto znalezione moduły:",
        'no_cards_in_module': "W tym module nie ma jeszcze kart.",
        'card_front': "{}",  # Текст для лицевой стороны карточки (иностранное слово)
        'card_back': "{}",  # Текст для обратной стороны карточки (перевод)
        'flip': "Obróć",
        'next': "Dalej",
        'all_cards_passed': "Przeszedłeś wszystkie karty!",
    },
    'zh': {
        'start_message': "你好！选择一种语言：",
        'register_message': "你好！ 看来您尚未注册。 单击下面的按钮进行注册。",
        'nickname_request': "请输入你的昵称：",
        'nickname_taken': "该昵称已被使用。 请选择另一个：",
        'password_request': "现在输入你的密码：",
        'registration_complete': "注册完成！",
        'main_menu': "主菜单",
        'start_learning': "✔ 开始学习",
        'create_module': "✔ 创建新模块",
        'bot_info': "ℹ 机器人信息",
        'how_to_use': "😦 如何使用机器人",
        'my_account': "👀 我的帐户",
        'back_to_main_menu': "⬅ 返回主菜单",
        'my_account_info': "你的id - {}\n"
                           "----------------------\n"
                           "昵称 - {}\n"
                           "注册日期 - {}\n"
                           "创建的卡片数量 - {}\n"
                           "-------------------------\n"
                           "评分 - {}\n"
                           "高级会员有效期至：{}",
        'how_to_use_info': "这是使用方法",
        'support': "支持",
        'start_learning_message': "太好了，让我们开始吧",
        'my_modules': "查看我的模块",
        'other_modules': "查看其他模块",
        'edit_modules_message': "这里写着一些东西，据说是说明",
        'create_module': "创建新模块",
        'edit_existing_module': "编辑现有模块",
        'bot_info_message': "这里是信息",
        'change_language': "更改语言",
        'register': "报名",
        'change_nickname': "更改昵称",
        'change_password': "更改密码",
        'get_premium': "获得高级会员",
        'activate_premium': "激活高级会员",
        'enter_new_nickname': "输入您要更改为当前昵称的昵称 - {}",
        'nickname_exists': "此昵称已存在，请输入另一个昵称",
        'enter_old_password': "输入您的旧密码以确认您的身份",
        'incorrect_password': "密码不正确，请重试",
        'enter_new_password': "输入新密码",
        'premium_link': "https://t.me/telegram",
        'enter_premium_key': "输入激活码",
        'invalid_premium_key': "❌ 密钥无效，请重试",
        'nickname_changed': "昵称已成功更改",
        'password_changed': "密码已成功更改",
        'premium_activated': "高级会员已成功激活至 {}",
        'premium_activated_message': "1个月的访问权限已激活",
        'select_original_language': "选择外语单词的编写语言",
        'select_translation_language': "选择模块中单词的翻译语言",
        'enter_module_name': "输入模块名称",
        'enter_module_description': "如果需要，请输入新模块的描述",
        'skip_description': "跳过",
        'description_too_long': "描述不得超过100个字符。 请再试一次.",
        'module_created_add_cards': "太好了，新模块已创建，要添加卡片来学习吗？",
        'add_cards': "💹 添加卡片",
        'enter_foreign_word': "输入外语单词 (最多 100 个字符):",
        'enter_translation': "输入单词的翻译 (最多 100 个字符):",
        'add_image_to_card': "为此卡添加图片？",
        'skip': "跳过",
        'add': "添加！",
        'card_saved_add_next': "卡片已成功保存，添加下一张还是返回主菜单？",
        'add_next_card': "添加下一张卡片",
        'invalid_image_format': "无效的图像格式。 请发送 JPEG 或 PNG 格式的图像。",
        'module_name_request': "输入要搜索的模块名称：",
        'no_modules_found': "未找到具有相似名称的模块。",
        'modules_found': "这是找到的模块：",
        'no_cards_in_module': "此模块中尚无卡片。",
        'card_front': "{}",  # Текст для лицевой стороны карточки (иностранное слово)
        'card_back': "{}",  # Текст для лицевой стороны карточки (перевод)
        'flip': "翻转",
        'next': "下一个",
        'all_cards_passed': "您已通过所有卡片！",
    },
    'ja': {
        'start_message': "こんにちは！言語を選択してください：",
        'register_message': "こんにちは！ まだ登録されていないようです。 登録するには、下のボタンをクリックしてください。",
        'nickname_request': "ニックネームを入力してください：",
        'nickname_taken': "このニックネームはすでに使用されています。 別のものを選択してください：",
        'password_request': "次にパスワードを入力してください：",
        'registration_complete': "登録完了！",
        'main_menu': "メインメニュー",
        'start_learning': "✔ 学習を開始する",
        'create_module': "✔ 新しいモジュールを作成する",
        'bot_info': "ℹ ボット情報",
        'how_to_use': "😦 ボットの使い方",
        'my_account': "👀 私のアカウント",
        'back_to_main_menu': "⬅ メインメニューに戻る",
        'my_account_info': "あなたのID - {}\n"
                           "----------------------\n"
                           "ニックネーム - {}\n"
                           "登録日 - {}\n"
                           "作成されたカードの数 - {}\n"
                           "-------------------------\n"
                           "評価 - {}\n"
                           "プレミアムは{}まで有効です",
        'how_to_use_info': "使い方はこちらです",
        'support': "サポート",
        'start_learning_message': "素晴らしい、始めましょう",
        'my_modules': "自分のモジュールを表示する",
        'other_modules': "他のモジュールを表示する",
        'edit_modules_message': "ここに何か書いてありますが、説明書だそうです",
        'create_module': "新しいモジュールを作成する",
        'edit_existing_module': "既存のモジュールを編集する",
        'bot_info_message': "ここに情報があります",
        'change_language': "言語を変更する",
        'register': "登録",
        'change_nickname': "ニックネームを変更する",
        'change_password': "パスワードを変更する",
        'get_premium': "プレミアムを入手する",
        'activate_premium': "プレミアムを有効にする",
        'enter_new_nickname': "現在のニックネームを変更したいニックネームを入力してください - {}",
        'nickname_exists': "このニックネームはすでに存在します。別のニックネームを入力してください",
        'enter_old_password': "身元を確認するために古いパスワードを入力してください",
        'incorrect_password': "パスワードが間違っています。もう一度お試しください",
        'enter_new_password': "新しいパスワードを入力してください",
        'premium_link': "https://t.me/telegram",
        'enter_premium_key': "アクティベーションキーを入力してください",
        'invalid_premium_key': "❌ 無効なキーです。もう一度お試しください",
        'nickname_changed': "ニックネームが正常に変更されました",
        'password_changed': "パスワードが正常に変更されました",
        'premium_activated': "プレミアムは{}まで正常にアクティブ化されました",
        'premium_activated_message': "1か月間のアクセスが有効になりました",
        'select_original_language': "外国語の単語を記述する言語を選択してください",
        'select_translation_language': "モジュール内の単語を翻訳する言語を選択してください",
        'enter_module_name': "モジュールの名前を入力してください",
        'enter_module_description': "必要に応じて、新しいモジュールの説明を入力してください",
        'skip_description': "スキップ",
        'description_too_long': "説明は100文字以内でなければなりません。 もう一度お試しください。",
        'module_created_add_cards': "素晴らしい、新しいモジュールが作成されました。学習用のカードを追加しますか？",
        'add_cards': "💹 カードを追加",
        'enter_foreign_word': "外国語の単語を入力してください (最大 100 文字):",
        'enter_translation': "単語の翻訳を入力してください (最大 100 文字):",
        'add_image_to_card': "このカードに画像を追加しますか？",
        'skip': "スキップ",
        'add': "追加！",
        'card_saved_add_next': "カードが正常に保存されました。次のカードを追加しますか、それともメインメニューに戻りますか？",
        'add_next_card': "次のカードを追加",
        'invalid_image_format': "無効な画像形式です。 JPEGまたはPNG形式で画像を送信してください。",
        'module_name_request': "検索するモジュール名を入力してください:",
        'no_modules_found': "類似の名前のモジュールは見つかりませんでした。",
        'modules_found': "見つかったモジュールはこちらです:",
        'no_cards_in_module': "このモジュールにはまだカードがありません。",
        'card_front': "{}",  # Текст для лицевой стороны карточки (иностранное слово)
        'card_back': "{}",  # Текст для лицевой стороны карточки (перевод)
        'flip': "フリップ",
        'next': "次へ",
        'all_cards_passed': "すべてのカードを渡しました！",
    },
}


def generate_unique_module_id():
    while True:
        new_id = random.randint(100000000000000, 999999999999999)
        # Проверяем, существует ли уже такой ID в базе данных
        existing_module = session.query(Collection).filter_by(id=new_id).first()
        if not existing_module:
            return new_id


def get_text(language, key, *args):
    try:
        return texts.get(language, texts['ru']).get(key, 'Текст не найден').format(*args)
    except Exception as e:
        print(f"Error formatting text: {e}")
        return texts.get(language, texts['ru']).get(key, 'Текст не найден')


def create_main_menu_keyboard(language):
    return [
        [Button.inline(get_text(language, 'start_learning'), data=b"start_learning")],
        [Button.inline(get_text(language, 'create_module'), data=b"create_module")],
        [Button.inline(get_text(language, 'bot_info'), data=b"bot_info"),
         Button.inline(get_text(language, 'how_to_use'), data=b"how_to_use")],
        [Button.inline(get_text(language, 'my_account'), data=b"my_account")]
    ]


def create_back_to_main_menu_keyboard(language):
    return [
        [Button.inline(get_text(language, 'back_to_main_menu'), data=b"back_to_main_menu")]
    ]


def create_learning_menu_keyboard(language):
    return [
        [Button.inline(get_text(language, 'my_modules'), data=b"my_modules")],
        [Button.inline(get_text(language, 'other_modules'), data=b"other_modules")],
        [Button.inline(get_text(language, 'back_to_main_menu'), data=b"back_to_main_menu")]
    ]


def create_edit_modules_keyboard(language):
    return [
        [Button.inline(get_text(language, 'create_module'), data=b"create_module")],
        [Button.inline(get_text(language, 'edit_existing_module'), data=b"edit_existing_module")],
        [Button.inline(get_text(language, 'back_to_main_menu'), data=b"back_to_main_menu")]
    ]


def create_language_selection_keyboard():
    return [
        [Button.inline("🇷🇺 Русский", data=b"lang_ru"), Button.inline("🇬🇧 English", data=b"lang_en")],
        [Button.inline("🇺🇦 Українська", data=b"lang_uk"), Button.inline("🇵🇱 Polski", data=b"lang_pl")],
        [Button.inline("🇨🇳 中文", data=b"lang_zh"), Button.inline("🇯🇵 日本語", data=b"lang_ja")]
    ]


def create_my_account_keyboard(language):
    return [
        [
            Button.inline(get_text(language, 'change_nickname'), data=b"change_nickname"),
            Button.inline(get_text(language, 'change_password'), data=b"change_password")
        ],
        [
            Button.url(get_text(language, 'get_premium'), url='https://t.me/telegram'),
            Button.inline(get_text(language, 'activate_premium'), data=b"activate_premium")
        ],
        [
            Button.inline(get_text(language, 'change_language'), data=b"change_language")
        ],
        create_back_to_main_menu_keyboard(language)[0]
    ]


# Добавим функцию для создания клавиатуры выбора языка с кнопкой "Назад в главное меню"
def create_language_selection_keyboard_with_back():
    keyboard = create_language_selection_keyboard()
    keyboard.append([Button.inline("⬅ Назад в главное меню", data=b"back_to_main_menu")])
    return keyboard


def create_add_cards_keyboard(language):
    return [
        [Button.inline(get_text(language, 'add_cards'), data=b"add_cards_action")],
        create_back_to_main_menu_keyboard(language)[0]
    ]


def create_add_image_keyboard(language):
    return [
        [Button.inline(get_text(language, 'skip'), data=b"skip_image"),
         Button.inline(get_text(language, 'add'), data=b"add_image")]
    ]


def create_card_saved_keyboard(language):
    return [
        [Button.inline(get_text(language, 'add_next_card'), data=b"add_next_card_action")],
        create_back_to_main_menu_keyboard(language)[0]
    ]


def create_module_keyboard(language, module_id):
    return [
        [Button.inline(get_text(language, 'flip'), data=f"flip_{module_id}")],
        [Button.inline(get_text(language, 'next'), data=f"next_{module_id}")],
        [Button.inline(get_text(language, 'back_to_main_menu'), data=b"back_to_main_menu")]
    ]


@client.on(events.CallbackQuery(data=b"my_account"))
async def my_account_handler(event):
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

    account_info = get_text(language, 'my_account_info', user_id, nick, date, count_of_cards, rating, premium_date)

    await client.edit_message(event.chat_id, event.message_id, account_info,
                              buttons=create_my_account_keyboard(language), file=MY_ACC_IMG_PATH)


@client.on(events.CallbackQuery(data=b"change_language"))
async def change_language_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await event.edit(get_text(language, 'change_language'), buttons=create_language_selection_keyboard())


@client.on(events.CallbackQuery(pattern=b"lang_.*"))
async def language_selection_handler(event):
    user_id = event.sender_id
    language = event.data.decode('utf-8').split('_')[1]
    user_tg = session.query(UserTg).filter_by(id=user_id).first()

    if not user_tg:
        # Если нет информации о пользователе, создаем
        user_tg = UserTg(id=user_id, username=event.sender.username or "NO_USERNAME", date=datetime.datetime.now())
        session.add(user_tg)
        session.commit()

    user_tg.language = language
    session.commit()

    user_bot = session.query(UserBot).filter_by(id=user_id).first()
    if user_bot:
        await send_main_menu(event)
    else:
        # Отправляем новое сообщение с предложением зарегистрироваться
        await client.send_message(event.chat_id, get_text(language, 'register_message'),
                                  buttons=[[Button.inline(get_text(language, 'register'), data=b"Register")]])


@client.on(events.CallbackQuery(pattern=b"module_lang_.*"))
async def module_language_selection_handler(event):
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


@client.on(events.CallbackQuery(data=b"start_learning"))
async def start_learning_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'start_learning_message'),
                              buttons=create_learning_menu_keyboard(language), file=STARS_LEARN_IMG_PATH)


@client.on(events.CallbackQuery(data=b"how_to_use"))
async def how_to_use_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'how_to_use_info'),
                              buttons=[[Button.url(get_text(language, 'support'), url='https://t.me/telegram')],
                                       create_back_to_main_menu_keyboard(language)[0]], file=HOW_TO_USE_IMG_PATH)


@client.on(events.CallbackQuery(data=b"create_module"))
async def edit_modules_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'edit_modules_message'),
                              buttons=create_edit_modules_keyboard(language), file=CREATE_NEW_IMG_PATH)


@client.on(events.CallbackQuery(data=b"add_cards_action"))  # Изменено data
async def add_cards_action_handler(event):  # Переименовано название функции
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'

    if user_id in card_creation_state:
        # Устанавливаем состояние ожидания ввода иностранного слова
        card_creation_state[user_id]["state"] = "waiting_for_foreign_word"
        # await event.edit(event.chat_id, event.message_id, get_text(language, 'enter_foreign_word')) #  Заменено
        await client.send_message(event.chat_id, get_text(language, 'enter_foreign_word'))  # Отправляем новое сообщение


@client.on(events.CallbackQuery(data=b"bot_info"))
async def bot_info_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'bot_info_message'),
                              buttons=create_back_to_main_menu_keyboard(language), file=INFO_IMG_PATH)


@client.on(events.CallbackQuery(data=b"back_to_main_menu"))
async def back_to_main_menu_handler(event):
    await send_main_menu(event)


async def send_main_menu(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'main_menu'),
                              buttons=create_main_menu_keyboard(language), file=MAIN_MENU_IMG_PATH)


registration_state = {}
change_nickname_state = {}
change_password_state = {}
activate_premium_state = {}
password_required_after_menu = {}

# Добавим словарь для хранения состояния создания модуля
module_creation_state = {}

# Добавим словарь для хранения состояния создания карточек
card_creation_state = {}

# Состояние просмотра модулей
module_view_state = {}

# Добавим словарь для хранения message_id карточек для их последующего обновления
card_message_ids = {}

# Добавим словарь для хранения языковых кодов
language_codes = {
    'ru': 'ru',
    'en': 'en',
    'uk': 'ukr',
    'pl': 'pol',
    'zh': 'chin',
    'ja': 'jap'
}


@client.on(events.CallbackQuery(data=b"create_module"))
async def create_module_handler(event):
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


@client.on(events.CallbackQuery(pattern=b"lang_.*"))
async def language_selection_handler(event):
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
                                          buttons=[[Button.inline(get_text(language, 'register'), data=b"Register")]])


@client.on(events.NewMessage)
async def handle_messages(event):
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

            # del change_password_state[user_id]
            # password_required_after_menu[user_id] = False

            await event.respond(get_text(language, 'password_changed'),
                                buttons=create_back_to_main_menu_keyboard(language))

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
                                    [Button.inline(get_text(language, 'skip_description'), data=b"skip_description")]])

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
            module_buttons = [[Button.inline(module.name, data=f"view_module_{module.id}")] for module in modules]
            module_buttons.append(create_back_to_main_menu_keyboard(language)[0])
            await event.respond(get_text(language, 'modules_found'), buttons=module_buttons)
        else:
            await event.respond(get_text(language, 'no_modules_found'),
                                buttons=create_back_to_main_menu_keyboard(language))

        # Очищаем состояние
        del module_view_state[user_id]


async def send_main_menu_new_message(event):  # Новая функция для отправки нового сообщения
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    await client.send_file(event.chat_id, MAIN_MENU_IMG_PATH, caption=get_text(language, 'main_menu'),
                           buttons=create_main_menu_keyboard(language))


@client.on(events.CallbackQuery(data=b"skip_description"))
async def skip_description_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'

    if user_id in module_creation_state and module_creation_state[user_id]["state"] == "waiting_for_module_description":
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


@client.on(events.CallbackQuery(data=b"change_nickname"))
async def change_nickname_handler(event):
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


@client.on(events.CallbackQuery(data=b"change_password"))
async def change_password_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    change_password_state[user_id] = "waiting_for_old_password"
    await event.respond(get_text(language, 'enter_old_password'),
                        buttons=create_back_to_main_menu_keyboard(language))


@client.on(events.CallbackQuery(data=b"activate_premium"))
async def activate_premium_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    activate_premium_state[user_id] = "waiting_for_premium_key"
    await event.respond(get_text(language, 'enter_premium_key'),
                        buttons=create_back_to_main_menu_keyboard(language))


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
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
                await send_main_menu(event)
        else:
            await event.respond(get_text(language, 'register_message'),
                                buttons=[[Button.inline(get_text(language, 'register'), data=b"Register")]])


@client.on(events.CallbackQuery(data=b"Register"))
async def registration_button(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'
    registration_state[user_id] = "waiting_for_nickname"
    await event.respond(get_text(language, 'nickname_request'))


@client.on(events.CallbackQuery(data=b"skip_image"))
async def skip_image_handler(event):
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


@client.on(events.CallbackQuery(data=b"add_image"))
async def add_image_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'

    if user_id in card_creation_state and card_creation_state[user_id]["state"] == "waiting_for_image_choice":
        # Переходим в состояние ожидания изображения
        card_creation_state[user_id]["state"] = "waiting_for_image"
        await client.edit_message(event.chat_id, event.message_id, "Пожалуйста, отправьте изображение для карточки.")


@client.on(events.NewMessage(pattern=None, func=lambda e: e.photo or e.document))
async def image_handler(event):
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
            await client.edit_message(event.chat_id, event.message_id, get_text(language, 'card_saved_add_next'),
                                      buttons=create_card_saved_keyboard(language))

        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")


@client.on(events.CallbackQuery(data=b"add_next_card_action"))  # Изменено data
async def add_next_card_action_handler(event):  # Переименовано название функции
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'

    if user_id in card_creation_state:
        # Устанавливаем состояние ожидания ввода иностранного слова
        card_creation_state[user_id]["state"] = "waiting_for_foreign_word"
        await client.send_message(event.chat_id, get_text(language, 'enter_foreign_word'))  # Отправляем новое сообщение


# Обработчики для просмотра модулей и карточек
@client.on(events.CallbackQuery(data=b"my_modules"))
async def my_modules_handler(event):
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


@client.on(events.CallbackQuery(data=b"other_modules"))
async def other_modules_handler(event):
    user_id = event.sender_id
    user_tg = session.query(UserTg).filter_by(id=user_id).first()
    language = user_tg.language if user_tg else 'ru'

    # Устанавливаем состояние ожидания ввода названия модуля
    module_view_state[user_id] = {'state': 'waiting_for_module_name'}
    await client.edit_message(event.chat_id, event.message_id, get_text(language, 'module_name_request'),
                              buttons=create_back_to_main_menu_keyboard(language))


@client.on(events.CallbackQuery(pattern=r"view_module_(\d+)"))
async def view_module_handler(event):
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


async def show_card(event, user_id):
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
                                  buttons=create_back_to_main_menu_keyboard(language))  # Отправляем новое сообщение
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
        await event.respond(text, buttons=keyboard)  # Отправляем только текст, если не удалось отправить изображение


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
        state['card_face'] = 'front'
        await show_card(event, user_id)


async def main():
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
