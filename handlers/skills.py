# -*- coding: utf-8 -*-
"""This module contains handlers for bot skills.

Now there are only tasks here.
"""

from aiogram import types
import os
import json

from static import message_start
from core import dp, States, KEYBOARDS
from tools.keyboard import make_keyboard


@dp.message_handler(lambda message: message.text == "Дела",
                    state=States.SKILLS)
async def tasks_handler(message):
    """Handle switching to tasks.

    Switches the state from SKILLS to TASKS.

    Creates empty tasks file if it doesn't exist.
    Creates a keyboard (free or busy) with a task interface.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)

    filename = f'{user}_tasks.json'
    if filename not in os.listdir():
        data = {'name': [],
                'start': [],
                'end': [],
                'time': []}

    else:
        with open(filename, 'r') as f:
            data = json.load(f)
            # print("create data")

    if len(data['name']) == len(data['end']):
        message_text = "Сейчас вы ничем не заняты."
        poll_keyboard = make_keyboard(KEYBOARDS["free_tasks"])

    else:
        message_text = f"Сейчас вы заняты: {data['name'][-1]}"
        poll_keyboard = make_keyboard(KEYBOARDS["busy_tasks"])

    await message.answer(message_text, reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.SKILLS)
async def skills_revert_handler(message):
    """Handle a return to the start from the skills.

    Switches the state from SKILLS to START.

    Creates keyboard with all the start questions.

    """
    await dp.current_state(user=message.chat.id).set_state(States.START)

    await message.answer(message_start,
                         reply_markup=make_keyboard(KEYBOARDS["start"]))
