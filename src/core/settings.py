import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from read_messages import read_messages

load_dotenv()

logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


bot_messages = read_messages("response_messages.json")