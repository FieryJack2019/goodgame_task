from aiogram import types
from bot import states, keyboards
from bot.utils import text
from aiogram.dispatcher import FSMContext
from bot.utils.api import get_users, get_game, get_user
from main import send_like_message
from random import choice
from bot.handlers.menu import start_search

    
async def select_category(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    if call.data != 'back':
        await call.message.edit_text(text.SEARCH_GAME_SELECT, 
                                     reply_markup=keyboards.account.keyboard_games(int(call.data)))
        await states.search.SearchState.SELECT_GAME.set()
    else:
        await call.message.edit_text(text.MAIN_MENU, 
                                     reply_markup=keyboards.menu.keyboard_menu(stateData.get('userId')))
        await states.menu.MenuState.MENU.set()
    await call.answer()


async def select_game(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back':
        await state.update_data(serchGameId=int(call.data))
        await states.search.SearchState.SEARCH.set()
        await search_players(call, state)
    else:
        await start_search(call, state)
    await call.answer()


async def search_players(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    if call.data != 'back':
        listShownPlayer = stateData.get('listShownPlayer', [])
        findPlayer = get_users(stateData['serchGameId'], stateData['userId'], listShownPlayer)
        if findPlayer:
            randomPlayer = choice(findPlayer)
            listShownPlayer.append(randomPlayer['id'])
            await state.update_data(listShownPlayer=listShownPlayer)
            messageText = choice(text.SEARCH_MEM) + text.SEARCH_PLAYER.format(randomPlayer['nicknameSteam'],
                                                                            get_game(randomPlayer['mainGame'])['name'],
                                                                            randomPlayer['aboutMe'])
            await call.message.edit_text(messageText, reply_markup=keyboards.search.keyboard_search(randomPlayer['telegramID']))
        else:
            await call.message.edit_text(text.SEARCH_NOT_FOUND, reply_markup=keyboards.search.BACK_KEYBOARD)
    else:
        await call.message.edit_text(text.MAIN_MENU, 
                                     reply_markup=keyboards.menu.keyboard_menu(stateData.get('userId')))
        await states.menu.MenuState.MENU.set()
    await call.answer()


async def like_player(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    username = get_user(stateData['userId'])['telegramUsername']
    sendData = await send_like_message(int(call.data), username)
    if sendData:
        await call.message.edit_text(text.SEARCH_LIKE, reply_markup=keyboards.search.LIKE_KEYBOARD)
    else:
        await call.message.edit_text(text.SEARCH_LIKE_ERROR, reply_markup=keyboards.search.LIKE_KEYBOARD)
    await call.answer()