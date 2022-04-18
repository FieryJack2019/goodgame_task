from aiogram import types
from bot import states, keyboards
from bot.utils import text
from aiogram.dispatcher import FSMContext
from bot.utils.api import get_game, update_user, get_user


async def start_message(message: types.Message, state: FSMContext):
    stateData = await state.get_data()
    if not stateData.get('userId', None):
        if message.from_user.username:
            await state.update_data(userData={
                'telegramID': message.chat.id,
                'telegramUsername': message.from_user.username,
                'isActive': True
            })
            await message.answer(text.START_MESSAGE_FOR_NEW)
            await states.account.AccountRegisterState.INPUT_STEAM.set()
        else:
            await message.answer(text.ERROR_USERNAME)
    else:
        await message.answer(text.MAIN_MENU, 
                             reply_markup=keyboards.menu.keyboard_menu(stateData.get('userId')))
        await states.menu.MenuState.MENU.set()


async def start_search(call: types.CallbackQuery, state: FSMContext):
    dataCategory = keyboards.account.keyboard_categrory()
    await call.message.edit_text(text.SEARCH_CATEGORY_SELECT, 
                         reply_markup=dataCategory[0])
    await states.search.SearchState.SELECT_CATEGORY.set()
    await call.answer()

    
async def profile(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    userData = get_user(stateData['userId'])
    await call.message.edit_text(text.PROFILE.format(
                                 userData['nicknameSteam'],
                                 userData['aboutMe'],
                                 get_game(userData['mainGame'])['name']
                                ), reply_markup=keyboards.account.ACCOUNT_EDIT)
    await states.account.AccountEditState.SELECT_FIELD.set()
    await call.answer()


async def on_off_profile(call: types.CallbackQuery, state: FSMContext):
    stateData = await state.get_data()
    if call.data == 'deleteProfile':
        update_user(stateData['userId'], {'isActive': False})
        await call.message.edit_text(text.DELETE_PROFILE,
                                     reply_markup=keyboards.menu.keyboard_menu(stateData.get('userId')))
    elif call.data == 'returnProfile':
        update_user(stateData['userId'], {'isActive': True})
        await call.message.edit_text(text.RETURN_PROFILE,
                                     reply_markup=keyboards.menu.keyboard_menu(stateData.get('userId')))
    await call.answer()