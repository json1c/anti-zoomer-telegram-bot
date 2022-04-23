from dispatcher import dp, bot, db
from aiogram import types
from modules.templates import get_template


@dp.message_handler(commands="words")
async def cmd_words(message: types.Message):
    local_words_template = "Слова, запрещенные в вашем чате:\n"

    for word in db.get_all_local_words(message.chat.id):
        local_words_template += f"- {word}\n"
    
    await message.answer(local_words_template)

    whitelisted_words_template = "Слова-исключения:\n"
    
    for word in db.get_all_whitelisted_words(message.chat.id):
        whitelisted_words_template += f"- {word}\n"
    
    await message.answer(whitelisted_words_template)


@dp.message_handler(commands=["addword"])
async def cmd_addword(message: types.Message):
    args = message.text.split()

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if not member.is_chat_admin():
        await message.answer(get_template("administrative:not_enough_rights"))
        return

    if len(args) == 1:
        await message.answer(get_template("commands:addword:not_enough_arguments"))
    
    else:
        db.add_local_word(message.chat.id, args[1], message.from_user.id)
        await message.answer(get_template("commands:addword:success"))


@dp.message_handler(commands=["delword"])
async def cmd_delword(message: types.Message):
    args = message.text.split()

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if not member.is_chat_admin():
        await message.answer(get_template("administrative:not_enough_rights"))
        return

    if len(args) == 1:
        await message.answer(get_template("commands:delword:not_enough_arguments"))
    
    else:
        db.delete_local_word(message.chat.id, args[1])
        await message.answer(get_template("commands:delword:success"))


@dp.message_handler(commands=["addwhitelist"])
async def cmd_addwhitelist(message: types.Message):
    args = message.text.split()

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if not member.is_chat_admin():
        await message.answer(get_template("administrative:not_enough_rights"))
        return

    if len(args) == 1:
        await message.answer(get_template("commands:addwhitelist:not_enough_arguments"))
    
    else:
        db.add_word_to_whitelist(message.chat.id, args[1], message.from_user.id)
        await message.answer(get_template("commands:addwhitelist:success"))


@dp.message_handler(commands=["delwhitelist"])
async def cmd_delwhitelist(message: types.Message):
    args = message.text.split()

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if not member.is_chat_admin():
        await message.answer(get_template("administrative:not_enough_rights"))
        return

    if len(args) == 1:
        await message.answer(get_template("commands:delwhitelist:not_enough_arguments"))
    
    else:
        db.delete_word_from_whitelist(message.chat.id, args[1])
        await message.answer(get_template("commands:delwhitelist:success"))


