from dispatcher import dp, db
from aiogram import types
from modules.templates import get_template
from transliterate import translit


@dp.message_handler(chat_type="supergroup")
async def message(message: types.Message):
    for word in message.text.split():
        transliterated_word = translit(word, "ru")
        if db.check_word(message.chat.id, transliterated_word.lower()):
            await message.delete()

            await message.answer(
                get_template("administrative:message_deleted")
                .format(name=message.from_user.first_name, word=word)
            )
