import transliterate
from dispatcher import dp, words_db, chats_db, bot
from aiogram import types
from modules.templates import get_template
from modules.transliterator import Transliterator

transliterator = Transliterator()


@dp.message_handler(chat_type=["supergroup", "megagroup", "group"])
async def message(message: types.Message):
    if not chats_db.is_chat_exists_in_db(message.chat.id):
        chats_db.insert_new_chat(message.chat.id)

    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if member.is_chat_admin():
        if not chats_db.get_admin_delete(message.chat.id):
            return
    
    for word in message.text.split():
        transliterated_word = transliterator.transliterate(word)
        if words_db.check_word(message.chat.id, transliterated_word.lower()):
            await message.delete()

            await message.answer(
                get_template("administrative:message_deleted")
                .format(name=message.from_user.first_name, word=word)
            )
