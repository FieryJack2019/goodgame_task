from aiogram import types
from bot.utils.api import get_category, get_games


def keyboard_categrory() -> tuple:
    keyboard = types.InlineKeyboardMarkup()
    description = {}
    for item in get_category():
        keyboard.add(types.InlineKeyboardButton(item['name'], callback_data=str(item['id'])))
        description[item['id']] = item['description']
    keyboard.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back'))
    return (keyboard, description)


def keyboard_games(categoryId: int) -> types.InlineKeyboardMarkup():
    keyboard = types.InlineKeyboardMarkup()
    for item in get_games(categoryId):
        keyboard.add(types.InlineKeyboardButton(item['name'], callback_data=str(item['id'])))
    keyboard.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back'))
    return keyboard


ACCOUNT_EDIT = types.InlineKeyboardMarkup()
ACCOUNT_EDIT.add(types.InlineKeyboardButton('🎲 Никнейм Steam', callback_data='nicknameSteam'))
ACCOUNT_EDIT.add(types.InlineKeyboardButton('👨 О себе', callback_data='aboutMe'))
ACCOUNT_EDIT.add(types.InlineKeyboardButton('🕹 Основная игра', callback_data='mainGame'))
ACCOUNT_EDIT.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back'))