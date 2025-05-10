import asyncio
import os
from telethon import TelegramClient
from PIL import Image
from db_utils import engine, Base, Session
from handlers import register_handlers
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
    # Создаем пустой файл non_image.png, если его нет
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


client = TelegramClient('session_name', API_ID, API_HASH)


async def main():
    Base.metadata.create_all(engine)
    print("База данных успешно создана!")
    # Регистрируем обработчики
    register_handlers(client, Session, NON_IMAGE_PATH, MAIN_MENU_IMG_PATH, STARS_LEARN_IMG_PATH, CREATE_NEW_IMG_PATH,
                      INFO_IMG_PATH, HOW_TO_USE_IMG_PATH, MY_ACC_IMG_PATH)  # Передаем необходимые зависимости
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()