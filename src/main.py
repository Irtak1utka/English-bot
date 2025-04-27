import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from telethon import TelegramClient, events
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///db.sqlite"
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

api_id = '21496201'  # пока для тестов создал этот id и hash для авторизации. сменить, создав свои  через - https://my.telegram.org/apps
api_hash = 'd748b2e5537217317a5a74b7c902e3d7'
bot_token = ''

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    session = Session()
    user_id = event.sender_id
    user = session.query(User).filter_by(id=user_id).first()

    if user:
        await event.reply("Ты уже есть в базе, привет!")
    else:
        await event.reply("Пожалуйста, напишите свой username для прохождения регистрации.")

        @client.on(events.NewMessage(from_users=user_id))
        async def username_handler(event):
            username = event.raw_text
            exists = session.query(User).filter_by(username=username).first()

            if exists:
                await event.reply("Этот username уже занят, пожалуйста, используйте другой.")
            else:
                await event.reply("Придумайте пароль:")

                @client.on(events.NewMessage(from_users=user_id))
                async def password_handler(event):
                    password = event.raw_text

                    if validate_password(password):
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        new_user = User(id=user_id, username=username, password_hash=hashed_password)
                        session.add(new_user)
                        session.commit()
                        await event.reply("Регистрация завершена, добро пожаловать!")
                        client.remove_event_handler(username_handler)
                        client.remove_event_handler(password_handler)
                    else:
                        await event.reply("Придумайте пароль сложнее.")


def validate_password(password):
    """ Якобы для отбора пароля """
    if (len(password) < 8 or
            password.isalpha() or
            password.isdigit() or
            password in ['abcd', '12345', 'qwerty'] or
            not any(char in '!@#$%^&*()-+' for char in password)):
        return False
    return True


client.run_until_disconnected()
