from aiogram import types
from bot.utils.api import is_active_user


def keyboard_menu(userId):
    keyboard = types.InlineKeyboardMarkup()
    if is_active_user(userId):
        keyboard.add(types.InlineKeyboardButton('🔍 Начать поиск', callback_data='search'))
        keyboard.add(types.InlineKeyboardButton('👨 Моя анкета', callback_data='profile'))
        keyboard.add(types.InlineKeyboardButton('❌ Удалить анкету', callback_data='deleteProfile'))
    else:
        keyboard.add(types.InlineKeyboardButton('✅ Восстановить анкету', callback_data='returnProfile'))
    return keyboard


KEYBOARD_BACK = types.InlineKeyboardMarkup()
KEYBOARD_BACK.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back'))