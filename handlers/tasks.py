from aiogram import types
from core import dp, States, bot, TOKEN
from help_func import end_task, start_task, make_skills_keyboard, new_session, prepare_tasks_doc
import pandas as pd


@dp.message_handler(lambda message: message.text == "Завершить", state=States.S_TASKS)
async def end_task_handler(message):
    end_task(message.chat.id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
    poll_keyboard.add(types.KeyboardButton(text="Начать новую сессию"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer("Чем хотите заняться?", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == "Назад", state=States.S_TASKS)
async def revert_to_skills(message):
    await dp.current_state(user=message.chat.id).set_state(States.S_CHOOSE_SKILL)
    await message.answer("Выберите интересующую функцию", reply_markup=make_skills_keyboard())


@dp.message_handler(lambda message: message.text == "Получить данные",
                    state=States.S_TASKS)
async def download_tasks_handler(message):
    user = message.chat.id
    if prepare_tasks_doc(user) == 0:
        with open(f'{user}_tasks.xlsx', 'rb') as document:
            await bot.send_document(chat_id=user, document=document)
    else:
        await message.answer("Судя по моим данным, у вас еще не было активности.")


@dp.message_handler(lambda message: message.text == "Начать новую сессию",
                    state=States.S_TASKS)
async def new_session_handler(message):
    user = message.chat.id
    new_session(user)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
    poll_keyboard.add(types.KeyboardButton(text="Начать новую сессию"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer("Начата новая сессия. Чем хотите заняться?",
                         reply_markup=poll_keyboard)


@dp.message_handler(state=States.S_TASKS)
async def start_task_handler(message):
    user = message.chat.id
    start_task(message.text, user)
    # data = get_data(user)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    message_text = f"Сейчас вы заняты: {message.text}"
    await message.answer(message_text, reply_markup=poll_keyboard)
