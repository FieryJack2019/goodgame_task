import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.files import JSONStorage
from bot.data import config
from bot.utils import text
from pathlib import Path

from bot.states.account import AccountEditState, AccountRegisterState
from bot.states.menu import MenuState
from bot.states.search import SearchState


bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    storage = JSONStorage(f'{Path.cwd()}/{"fsm_data.json"}')
    dp = Dispatcher(bot, storage=storage)

    from bot.handlers import menu, account, search

    dp.register_message_handler(menu.start_message, commands=["start"], state="*")
    dp.register_message_handler(account.steam_input, state=AccountRegisterState.INPUT_STEAM)
    dp.register_message_handler(account.about_input, state=AccountRegisterState.INPUT_ABOUT)
    dp.register_callback_query_handler(account.about_back, lambda call: call.data == "back", state=AccountRegisterState.INPUT_ABOUT)
    dp.register_callback_query_handler(account.category_input, lambda call: call.data, state=AccountRegisterState.SELECT_CATEGORY)
    dp.register_callback_query_handler(account.game_input, lambda call: call.data, state=AccountRegisterState.SELECT_GAME)
    
    dp.register_callback_query_handler(menu.start_search, lambda call: call.data == "search", state=MenuState.MENU)
    dp.register_callback_query_handler(menu.profile, lambda call: call.data == "profile", state=MenuState.MENU)
    dp.register_callback_query_handler(menu.on_off_profile, lambda call: call.data in ["returnProfile", "deleteProfile"], state=MenuState.MENU)

    dp.register_callback_query_handler(account.select_edit_field, lambda call: call.data, state=AccountEditState.SELECT_FIELD)
    dp.register_callback_query_handler(account.cancle_edit, lambda call: call.data == 'back', state=AccountEditState.EDIT_FIELD)
    dp.register_message_handler(account.edit_field, state=AccountEditState.EDIT_FIELD)
    dp.register_callback_query_handler(account.category_select, lambda call: call.data, state=AccountEditState.EDIT_CATEGORY)
    dp.register_callback_query_handler(account.game_edit, lambda call: call.data, state=AccountEditState.EDIT_GAME)

    dp.register_callback_query_handler(search.select_category, lambda call: call.data, state=SearchState.SELECT_CATEGORY)
    dp.register_callback_query_handler(search.select_game, lambda call: call.data, state=SearchState.SELECT_GAME)
    dp.register_callback_query_handler(search.search_players, lambda call: call.data in ['back', 'nextSearch'], state=SearchState.SEARCH)
    dp.register_callback_query_handler(search.like_player, lambda call: call.data, state=SearchState.SEARCH)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


async def send_like_message(telegramID: int, username: str) -> bool:
    try:
        await bot.send_message(telegramID, text.SEARCH_MESSAGE.format(username))
        return True
    except:
        return False


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("BOT STOP")