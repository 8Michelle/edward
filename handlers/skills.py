from aiogram import types
from static import message_start
from core import dp, States
from help_func import make_start_keyboard, make_tasks_keyboard, make_busy_keyboard
import os
import json


@dp.message_handler(lambda message: message.text == "Назад", state=States.SKILLS)
async def skills_revert_handler(message):
    await dp.current_state(user=message.chat.id).set_state(States.START)
    await message.answer(message_start, reply_markup=make_start_keyboard())


@dp.message_handler(lambda message: message.text == "Дела", state=States.SKILLS)
async def tasks_handler(message):
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
        poll_keyboard = make_tasks_keyboard()
    else:
        message_text = f"Сейчас вы заняты: {data['name'][-1]}"
        poll_keyboard = make_busy_keyboard()

    await message.answer(message_text, reply_markup=poll_keyboard)
