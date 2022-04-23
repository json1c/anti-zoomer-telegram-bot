import logging
from unittest import skip

from aiogram import Bot
import handlers
from dispatcher import dp, bot
from aiogram.utils import executor
from aiogram.types import BotCommand, BotCommandScopeChat, ChatAdministratorRights

logging.basicConfig(level=logging.INFO)

async def set_my_commands(_):
    await bot.set_my_commands([
        BotCommand("addword", "Добавить слово для удаления"),
        BotCommand("delword", "Удалить слово из базы"),
        BotCommand("addwhitelist", "Добавить слово в исключения"),
        BotCommand("delwhitelist", "Удалить слово из исключений"),
        BotCommand("words", "Получить список слов-исключений и запрещенных локальных слов")
    ])

    await bot.set_my_default_administrator_rights(
        ChatAdministratorRights(
            can_delete_messages=True
        )
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_my_commands)
