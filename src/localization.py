import os

CARDS_FOLDER = "cards_folder"
main_language = "ru"
USUAL_IMG_FOLDER = os.path.join(CARDS_FOLDER, "usual_img_" + main_language)
NON_IMAGE_PATH = os.path.join(USUAL_IMG_FOLDER, "non_image.png")
MAIN_MENU_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "main_menu.png")
STARS_LEARN_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "stars_learn.png")
CREATE_NEW_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "create_new.png")
INFO_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "info.png")
HOW_TO_USE_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "how_to_use.png")
MY_ACC_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "my_acc.png")
file_paths = [USUAL_IMG_FOLDER, NON_IMAGE_PATH, MAIN_MENU_IMG_PATH, STARS_LEARN_IMG_PATH, CREATE_NEW_IMG_PATH,
              INFO_IMG_PATH, HOW_TO_USE_IMG_PATH, MY_ACC_IMG_PATH]

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
        'change_language': "Сменить язык🌍",
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
        'change_language': "Change language🌍",
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
        'change_language': "Змінити мову🌍",
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
        'change_language': "Zmień język🌍",
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
        'change_language': "更改语言🌍",
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
        'change_language': "言語を変更する🌍",
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


def get_text(language, key, *args):
    try:
        return texts.get(language, texts['ru']).get(key, 'Текст не найден').format(*args)
    except Exception as e:
        print(f"Error formatting text: {e}")
        return texts.get(language, texts['ru']).get(key, 'Текст не найден')


def translate_images(language):
    print(CREATE_NEW_IMG_PATH, "loc0")
    main_language = language
    CARDS_FOLDER = "cards_folder"
    USUAL_IMG_FOLDER = os.path.join(CARDS_FOLDER, "usual_img_" + main_language)
    NON_IMAGE_PATH = os.path.join(USUAL_IMG_FOLDER, "non_image.png")
    MAIN_MENU_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "main_menu.png")
    STARS_LEARN_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "stars_learn.png")
    CREATE_NEW_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "create_new.png")
    INFO_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "info.png")
    HOW_TO_USE_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "how_to_use.png")
    MY_ACC_IMG_PATH = os.path.join(USUAL_IMG_FOLDER, "my_acc.png")
    print(USUAL_IMG_FOLDER, "loc1")
    print(CREATE_NEW_IMG_PATH, "loc2")
    return CARDS_FOLDER, USUAL_IMG_FOLDER, NON_IMAGE_PATH, \
        MAIN_MENU_IMG_PATH, STARS_LEARN_IMG_PATH, CREATE_NEW_IMG_PATH, INFO_IMG_PATH, \
        HOW_TO_USE_IMG_PATH, MY_ACC_IMG_PATH
