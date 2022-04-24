import config
from modules.word_database import WordDatabase
from modules.chats_database import ChatsDatabase
from aiogram import Bot, Dispatcher

words_db = WordDatabase()
chats_db = ChatsDatabase()

bot = Bot(config.BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot)
