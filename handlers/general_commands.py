from aiogram import types
from core import dp, States
from help_func import make_start_keyboard, make_skills_keyboard
from static import message_skills, message_start, message_creator


@dp.message_handler(commands=['start'])
async def start_handler(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.START)
    await message.answer(message_start, reply_markup=make_start_keyboard())


@dp.message_handler(lambda message: message.text == "Что ты умеешь?", state=States.START)
async def skills_about_handler(message):
    await message.answer(message_skills)


@dp.message_handler(lambda message: message.text == "Кто тебя создал?", state=States.START)
async def creator(message):
    await message.answer(message_creator)


@dp.message_handler(lambda message: message.text == "Функции", state=States.START)
async def skills_handler(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.SKILLS)
    await message.answer("Выберите функцию", reply_markup=make_skills_keyboard())