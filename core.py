# -*- coding: utf-8 -*-
"""This module contains main bot structure and configuration.

There are logger settings, dispatcher, bot, states machine,
skills list and their parameters.

"""
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
    """This class realizes a state machine for the bot."""

    START = State()
    SKILLS = State()
    TASKS = State()
    BEGIN_TASK = State()
    NEW_SESSION = State()


SKILLS = ['Дела']


KEYBOARDS = {
    "start": ["Что ты умеешь?", "Кто тебя создал?", "Функции"],

    "skills": SKILLS + ["Назад"],

    "free_tasks": ["Начать дело", "Какое сегодня число?",
                   "Начать новую сессию", "Сколько я сегодня поработал?",
                   "Получить данные", "Назад"],

    "busy_tasks": ["Завершить", "Назад"],

    "new_session": ["Все верно", "Назад"]
}
