from aiogram.utils import markdown as md

templates = {
    "commands": {
        "start": "Привет, {name}!\n\nЯ бот, созданный для удаления сообщений, содердащих неприятные зумерские слова.\nПригласи меня в чат и дай право на удаление сообщений",
        "addword": {
            "not_enough_arguments": "Команда нужна для того, чтобы добавить слово в базу.\n\n/addword [тип: regexp | text] [слово]",
            "success": "Слово успешно добавлено"
        },
        "delword": {
            "not_enough_arguments": "Команда нужна для того, чтобы удалить слово из базы.\n\n/delword [слово]",
            "success": "Слово успешно удалено"
        },
        "addwhitelist": {
            "not_enough_arguments": "Команда нужна для того, чтобы добавить слово в исключения.\n\nНапример: /addwhitelist чел",
            "success": "Слово успешно добавлено в исключения"
        },
        "delwhitelist": {
            "not_enough_arguments": "Команда нужна для того, чтобы удалить слово из исключений.\n\n/delwhitelist чел",
            "success": "Слово успешно удалено из исключений"
        },
        "toggleadmindelete": {
            "toggled": {
                "true": "Теперь сообщения от админов удаляются",
                "false": "Теперь сообщения от админов не удаляются"
            }        
        }
        
    },
    "administrative": {
        "message_deleted": "{name}, ваше сообщение было удалено.\nПричина: зумерское слово ({word})",
        "not_enough_rights": "У вас недостаточно прав, чтобы совершить это действие"
    }
}

def get_template(key: str) -> str:
    """
    Get template by key
    """

    keys = key.split(":")

    index = 0
    value = templates[keys[index]]

    while isinstance(value, dict):
        index += 1
        value = value[keys[index]]

    return value
