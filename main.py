from aiogram import Dispatcher
from aiogram.utils import executor
from bot.src.core.settings import dp
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def on_startup(dp: Dispatcher):
    """
    Start the bot and run it in polling mode.
    """
    from bot.src.core.http_client import zoho_client
    from bot.src.handlers.client import (users_info,
                                         company_materials,
                                         career_strategy_handlers)

    users_info.register_handlers_client(dp)
    company_materials.register_handlers_client(dp)
    career_strategy_handlers.register_handlers_client(dp)
    await zoho_client.refresh_token()


async def on_shutdown(dp: Dispatcher):
    from bot.src.core.http_client import zoho_client

    await zoho_client.close()
    await dp.bot.close()
    await dp.storage.close()


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False
    )
