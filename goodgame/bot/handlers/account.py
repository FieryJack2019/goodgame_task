from aiogram import types
from bot import states, keyboards
from bot.utils import text
from aiogram.dispatcher import FSMContext
from bot.utils.api import add_new_user, update_user, get_user, get_game
from bot.handlers.menu import profile


async def steam_input(message: types.Message, state: FSMContext):
    stateData = await state.get_data()
    stateData['userData']['nicknameSteam'] = message.text
    await state.update_data(userData=stateData['userData'])
    await message.answer(text.ACCOUNT_ABOUT_ME, 
                         reply_markup=keyboards.menu.KEYBOARD_BACK)
    await states.account.AccountRegisterState.INPUT_ABOUT.set()


async def about_input(message: types.Message, state: FSMContext):
    stateData = await state.get_data()
    stateData['userData']['aboutMe'] = message.text
    dataCategory = keyboards.account.keyboard_categrory()
    await state.update_data(userData=stateData['userData'], dataCategory=dataCategory[1])
    await message.answer(text.ACCOUNT_CATEGORY, 
                         reply_markup=dataCategory[0])
    await states.account.AccountRegisterState.SELECT_CATEGORY.set()


async def about_back(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.ACCOUNT_STEAM)
    await states.account.AccountRegisterState.INPUT_STEAM.set()
    await call.answer()


async def category_input(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back':
        stateData = await state.get_data()
        await state.update_data(idCategory=int(call.data))
        await call.message.edit_text(text.ACCOUNT_GAME.format(stateData['dataCategory'][int(call.data)]), 
                                     reply_markup=keyboards.account.keyboard_games(int(call.data)))
        await states.account.AccountRegisterState.SELECT_GAME.set()
    else:
        await call.message.edit_text(text.ACCOUNT_ABOUT_ME,
                                     reply_markup=keyboards.menu.KEYBOARD_BACK)
        await states.account.AccountRegisterState.INPUT_ABOUT.set()
    await call.answer()


async def game_input(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    if call.data != 'back':
        stateData['userData']['mainGame'] = int(call.data)
        userId = add_new_user(stateData['userData'])
        await state.update_data(userId=userId, userData=stateData['userData'])
        await call.message.edit_text(text.ACCOUNT_COMPLETE, 
                                     reply_markup=keyboards.menu.keyboard_menu(userId))
        await states.menu.MenuState.MENU.set()
    else:
        await call.message.edit_text(text.ACCOUNT_CATEGORY,
                                     reply_markup=keyboards.account.keyboard_categrory()[0])
        await states.account.AccountRegisterState.SELECT_CATEGORY.set()
    await call.answer()


async def edit_field(message: types.Message, state: FSMContext):
    stateData = await state.get_data()
    userData = update_user(stateData['userId'], {stateData['selectEditField']: message.text})
    await message.answer(text.UPDATE_PROFILE + text.PROFILE.format(
                                             userData['nicknameSteam'],
                                             userData['aboutMe'],
                                             get_game(userData['mainGame'])['name']
                                             ), 
                         reply_markup=keyboards.account.ACCOUNT_EDIT)
    await states.account.AccountEditState.SELECT_FIELD.set()


async def cancle_edit(call: types.CallbackQuery, state: FSMContext):
    await profile(call, state)


async def category_select(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'back':
        stateData = await state.get_data()
        await call.message.edit_text(text.ACCOUNT_GAME.format(stateData['dataCategory'][int(call.data)]), 
                                     reply_markup=keyboards.account.keyboard_games(int(call.data)))
        await states.account.AccountEditState.EDIT_GAME.set()
    else:
        await profile(call, state)
    await call.answer()


async def game_edit(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    if call.data != 'back':
        update_user(stateData['userId'], data={'mainGame': int(call.data)})
        await profile(call, state)
    else:
        await call.message.edit_text(text.ACCOUNT_CATEGORY,
                                     reply_markup=keyboards.account.keyboard_categrory()[0])
        await states.account.AccountEditState.EDIT_CATEGORY.set()
    await call.answer()


async def select_edit_field(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    if call.data == 'mainGame':
        dataCategory = keyboards.account.keyboard_categrory()
        await state.update_data(userData=stateData['userData'], dataCategory=dataCategory[1], selectEditField=call.data)
        await call.message.edit_text(text.ACCOUNT_CATEGORY, reply_markup=dataCategory[0])
        await states.account.AccountEditState.EDIT_CATEGORY.set()
    elif call.data == 'nicknameSteam':
        await call.message.edit_text(text.ACCOUNT_STEAM, reply_markup=keyboards.menu.KEYBOARD_BACK)
        await state.update_data(selectEditField=call.data)
        await states.account.AccountEditState.EDIT_FIELD.set()
    elif call.data == 'aboutMe':
        await call.message.edit_text(text.ACCOUNT_ABOUT_ME, reply_markup=keyboards.menu.KEYBOARD_BACK)
        await state.update_data(selectEditField=call.data)
        await states.account.AccountEditState.EDIT_FIELD.set()
    else:
        await call.message.edit_text(text.MAIN_MENU, 
                                     reply_markup=keyboards.menu.keyboard_menu(stateData.get('userId')))
        await states.menu.MenuState.MENU.set()
    await call.answer()