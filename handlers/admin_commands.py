from dispatcher import dp, bot, words_db, chats_db
from aiogram import types
from modules.templates import get_template


@dp.message_handler(commands="toggleadmindelete")
async def cmd_toggleadmindelete(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if not member.is_chat_admin():
        await message.answer(get_template("administrative:not_enough_rights"))
        return

    setted_value = chats_db.toggle_admin_delete(message.chat.id)

    await message.answer(
        get_template(f"commands:toggleadmindelete:toggled:{setted_value}")
    )


@dp.message_handler(commands="words")
async def cmd_words(message: types.Message):
    local_words_template = "Слова, запрещенные в вашем чате:\n"

    for word in words_db.get_all_local_words(message.chat.id):
        local_words_template += f"- {word}\n"
    
    await message.answer(local_words_template)

    whitelisted_words_template = "Слова-исключения:\n"
    
    for word in words_db.get_all_whitelisted_words(message.chat.id):
        whitelisted_words_template += f"- {word}\n"
    
    await message.answer(whitelisted_words_template)


@dp.message_handler(commands=["addword"])
async def cmd_addword(message: types.Message):
    args = message.text.split()

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if not member.is_chat_admin():
        await message.answer(get_template("administrative:not_enough_rights"))
        return

    if len(args) < 3:
        await message.answer(get_template("commands:addword:not_enough_arguments"))
    
    else:
        if args[1] not in ("text", "regexp"):
            await message.answer(get_template("commands:addword:not_enough_arguments"))
            return

        words_db.add_local_word(message.chat.id, args[2], message.from_user.id, args[1])
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
        words_db.delete_local_word(message.chat.id, args[1])
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
        words_db.add_word_to_whitelist(message.chat.id, args[1], message.from_user.id)
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
        words_db.delete_word_from_whitelist(message.chat.id, args[1])
        await message.answer(get_template("commands:delwhitelist:success"))


