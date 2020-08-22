import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup


logging.basicConfig(level=logging.INFO)
TOKEN = "1197211678:AAFMXwjRZIyoCWc8qLvUPcq31t5hcCGG9Fk"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class States(StatesGroup):
    # S_START = State()
    # S_CHOOSE_SKILL = State()
    # S_TASKS = State()
    START = State()
    SKILLS = State()
    TASKS = State()
    BEGIN_TASK = State()
    NEW_SESSION = State()


SKILLS = ['Дела']