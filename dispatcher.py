import config
from modules.database import WordDatabase
from aiogram import Bot, Dispatcher

db = WordDatabase()

bot = Bot(config.BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot)
