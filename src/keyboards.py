from telethon import Button
from localization import get_text


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