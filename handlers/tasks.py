from aiogram import types
from core import dp, States, bot, TOKEN
from help_func import get_data, end_task, start_task, make_skills_keyboard
import pandas as pd


@dp.message_handler(lambda message: message.text == "Завершить", state=States.S_TASKS)
async def stop_task(message):
    end_task(message.chat.id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer("Чем хотите заняться?", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == "Назад", state=States.S_TASKS)
async def revert_to_skills(message):
    await dp.current_state(user=message.chat.id).set_state(States.S_CHOOSE_SKILL)
    await message.answer("Выберите интересующую функцию", reply_markup=make_skills_keyboard())


@dp.message_handler(lambda message: message.text == "Получить данные", state=States.S_TASKS)
async def download_tasks(message):
    user = message.chat.id
    data = pd.DataFrame(get_data(user)).loc[:, ['name', 'time']]
    data['time'] = pd.to_datetime(data['time'], unit='s') - pd.to_datetime(0)
    data.to_excel(f'{user}_tasks.xlsx', index=False)
    with open(f'{user}_tasks.xlsx', 'rb') as document:
        await bot.send_document(chat_id=user, document=document)


@dp.message_handler(state=States.S_TASKS)
async def create_task(message):
    user = message.chat.id
    start_task(message.text, user)
    data = get_data(user)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    message_text = f"Сейчас вы заняты: {data['name'][-1]}"
    await message.answer(message_text, reply_markup=poll_keyboard)
