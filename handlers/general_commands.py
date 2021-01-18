# -*- coding: utf-8 -*-
from aiogram import types
from core import dp, States, KEYBOARDS
from tools.keyboard import make_keyboard
from static import message_skills, message_start, message_creator


@dp.message_handler(commands=['start'])
async def start_handler(message):
    """Handles \\start command and creates keyboard with starts questions.
    Switches state to START. Allows to go to skills.

    Args:
        message (types.message.Message): start command.

    """
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.START)

    await message.answer(message_start,
                         reply_markup=make_keyboard(KEYBOARDS["start"]))


@dp.message_handler(lambda message: message.text == "Что ты умеешь?",
                    state=States.START)
async def skills_about_handler(message):
    """Handles question about bot skills.
    Corresponds to the START state.

    Args:
        message (types.message.Message): question about skills.

    """
    await message.answer(message_skills)


@dp.message_handler(lambda message: message.text == "Кто тебя создал?",
                    state=States.START)
async def creator(message):
    """Handles question about creator.
    Corresponds to the START state.

    Args:
        message (types.message.Message): question about creator.

    """
    await message.answer(message_creator)


@dp.message_handler(lambda message: message.text == "Функции",
                    state=States.START)
async def skills_handler(message):
    """Handles skills question and creates skills keyboard.
    Corresponds to the START state.
    Switches the state to SKILLS. Allows to go to all the bot skills.

    Args:
        message (types.message.Message): skills message.

    """
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.SKILLS)

    await message.answer("Выберите функцию",
                         reply_markup=make_keyboard(KEYBOARDS["skills"]))
