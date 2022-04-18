from aiogram import types


def keyboard_search(telegramId: str) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Next ➡️', callback_data='nextSearch'))
    keyboard.add(types.InlineKeyboardButton('Like 👍', callback_data=telegramId))
    keyboard.add(types.InlineKeyboardButton('Закончить поиск', callback_data='back'))
    return keyboard


LIKE_KEYBOARD = types.InlineKeyboardMarkup()
LIKE_KEYBOARD.add(types.InlineKeyboardButton('Next ➡️', callback_data='nextSearch'))
LIKE_KEYBOARD.add(types.InlineKeyboardButton('Закончить поиск', callback_data='back'))

BACK_KEYBOARD = types.InlineKeyboardMarkup()
BACK_KEYBOARD.add(types.InlineKeyboardButton('Закончить поиск', callback_data='back'))