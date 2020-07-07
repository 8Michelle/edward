from aiogram import types
from core import dp, States
from help_func import make_start_keyword, make_skills_keyboard
from static import message_skills, message_start, message_creator

@dp.message_handler(commands=['start'])
async def start(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.S_START)
    await message.answer(message_start, reply_markup=make_start_keyword())


@dp.message_handler(lambda message: message.text == "Что ты умеешь?", state=States.S_START)
async def skills_about(message):
    answer = message_skills
    await message.answer(answer)


@dp.message_handler(lambda message: message.text == "Кто тебя создал?", state=States.S_START)
async def creator(message):
    await message.answer(message_creator)


@dp.message_handler(lambda message: message.text == "Функции", state=States.S_START)
async def skills(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.S_CHOOSE_SKILL)
    await message.answer("Выберите интересующую функцию", reply_markup=make_skills_keyboard())