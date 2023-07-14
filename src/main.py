from aiogram.utils import executor
from core.settings import dp


def start_bot():
    """
    Start the bot and run it in polling mode.
    """
    from handlers.client import (users_info,
                                 company_materials,
                                 career_strategy_handlers)

    users_info.register_handlers_client(dp)
    company_materials.register_handlers_client(dp)
    career_strategy_handlers.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
