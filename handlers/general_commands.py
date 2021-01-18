# -*- coding: utf-8 -*-
"""This module contains handlers for general commands and questions.

This handles can answer a question about the bot and its skills.
"""

from aiogram import types

from core import dp, States, KEYBOARDS
from tools.keyboard import make_keyboard
from static import message_skills, message_start, message_creator


@dp.message_handler(commands=['start'])
async def start_handler(message):
    """Handles the /start command.

    Switches the state to START.

    Creates keyboard with start questions.

    """
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.START)

    await message.answer(message_start,
                         reply_markup=make_keyboard(KEYBOARDS["start"]))


@dp.message_handler(lambda message: message.text == "Что ты умеешь?",
                    state=States.START)
async def skills_about_handler(message):
    """Answers a question about bot skills.

    Corresponds to the START state.

    """
    await message.answer(message_skills)


@dp.message_handler(lambda message: message.text == "Кто тебя создал?",
                    state=States.START)
async def creator(message):
    """Answers a question about bot creator.

    Corresponds to the START state.

    """
    await message.answer(message_creator)


@dp.message_handler(lambda message: message.text == "Функции",
                    state=States.START)
async def skills_handler(message):
    """Handles switching to skills.

    Switches the state from START to SKILLS.

    Creates a keyboard with all the bot skills.

    """
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.SKILLS)

    await message.answer("Выберите функцию",
                         reply_markup=make_keyboard(KEYBOARDS["skills"]))
