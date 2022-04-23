from dispatcher import dp
from aiogram import types
from modules.templates import get_template

@dp.message_handler(commands="start", chat_type="private")
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("🤖 Добавить меня в чат", url="https://t.me/AntiZoomerBot?startgroup=start"))

    keyboard.row(
        types.InlineKeyboardButton("📢 Мой канал", url="https://t.me/huis_bn"),
        types.InlineKeyboardButton("🍩 Донат", url="https://qiwi.com/n/JSON1C")
    )

    keyboard.row(types.InlineKeyboardButton("</> Мой исходный код", url="https://github.com/json1c/anti-zoomer-telegram-bot"))

    await message.answer(
        get_template("commands:start").format(name=message.from_user.first_name),
        reply_markup=keyboard
    )
