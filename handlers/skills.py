# -*- coding: utf-8 -*-
from aiogram import types
from static import message_start
from core import dp, States, KEYBOARDS
from tools.keyboard import make_keyboard
import os
import json


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.SKILLS)
async def skills_revert_handler(message):
    """Handles returning to the START state from SKILLS.
    Corresponds to the SKILLS state.
    Creates keyboard with starts questions.

    Args:
        message (types.Message.message): returning message.

    """
    await dp.current_state(user=message.chat.id).set_state(States.START)

    await message.answer(message_start,
                         reply_markup=make_keyboard(KEYBOARDS["start"]))


@dp.message_handler(lambda message: message.text == "Дела",
                    state=States.SKILLS)
async def tasks_handler(message):
    """Handles tasks message.
    Switches the state to TASKS.
    Creates empty tasks file if it doesn't exist.
    Creates busy or tasks keyboard. Corresponds to the SKILLS state.
    Allows to go to all the task functions or busy-returning function.

    Args:
        message (types.Message.message): tasks message.

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
            print("create data")

    if len(data['name']) == len(data['end']):
        message_text = "Сейчас вы ничем не заняты."
        poll_keyboard = make_keyboard(KEYBOARDS["free_tasks"])

    else:
        message_text = f"Сейчас вы заняты: {data['name'][-1]}"
        poll_keyboard = make_keyboard(KEYBOARDS["busy_tasks"])

    await message.answer(message_text, reply_markup=poll_keyboard)
