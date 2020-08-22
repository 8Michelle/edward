from aiogram import types
from core import dp, States, bot, TOKEN
from help_func import end_task, start_task, make_skills_keyboard,\
    new_session, prepare_tasks_doc, make_tasks_keyboard, make_new_session_keyboard,\
    make_busy_keyboard, make_begin_task_keyboard, get_working_time
import datetime
import pandas as pd


@dp.message_handler(lambda message: message.text == "Завершить",
                    state=States.TASKS)
async def end_task_handler(message):
    end_task(message.chat.id)
    await message.answer("Сейчас вы ничем не заняты.",
                         reply_markup=make_tasks_keyboard())


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.TASKS)
async def tasks_revert_handler(message):
    await dp.current_state(user=message.chat.id).set_state(States.SKILLS)
    await message.answer("Выберите функцию",
                         reply_markup=make_skills_keyboard())


@dp.message_handler(lambda message: message.text == "Начать новую сессию",
                    state=States.TASKS)
async def new_session_handler(message):
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.NEW_SESSION)
    date = datetime.date.today().isoformat()
    await message.answer(f"Новая дата {date.replace('-', '.')}?",
                         reply_markup=make_new_session_keyboard())


@dp.message_handler(lambda message: message.text == "Все верно",
                    state=States.NEW_SESSION)
async def new_session_submit_handler(message):
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)
    date = datetime.date.today().isoformat()
    new_session(user=user, date=date)
    await message.answer("Начата новая сессия. Сейчас вы ничем не заняты.",
                         reply_markup=make_tasks_keyboard())


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.NEW_SESSION)
async def new_session_revert_handler(message):
    await dp.current_state(user=message.chat.id).set_state(States.TASKS)
    await message.answer("Сейчас вы ничем не заняты.",
                         reply_markup=make_tasks_keyboard())


@dp.message_handler(state=States.NEW_SESSION)
async def new_session_date_handler(message):
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)
    new_session(user=user, date=message.text.replace('.', '-'))
    await message.answer(f"Начата новая сессия {message.text}. Сейчас вы ничем не заняты.",
                         reply_markup=make_tasks_keyboard())


@dp.message_handler(lambda message: message.text == "Начать дело", state=States.TASKS)
async def begin_task_handler(message):
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.BEGIN_TASK)
    await message.answer("Чем займетесь?",
                         reply_markup=make_begin_task_keyboard(user))


@dp.message_handler(lambda message: message.text == "Назад", state=States.BEGIN_TASK)
async def begin_task_revert_handler(message):
    await dp.current_state(user=message.chat.id).set_state(States.TASKS)
    await message.answer("Сейчас вы ничем не заняты",
                         reply_markup=make_tasks_keyboard())


@dp.message_handler(state=States.BEGIN_TASK)
async def begin_task_start_handler(message):
    user = message.chat.id
    start_task(message.text, user)
    await dp.current_state(user=user).set_state(States.TASKS)
    message_text = f"Сейчас вы заняты: {message.text}"
    await message.answer(message_text, reply_markup=make_busy_keyboard())


# --------------------- Обработка данных ---------------------------

@dp.message_handler(lambda message: message.text == "Получить данные",
                    state=States.TASKS)
async def download_tasks_handler(message):
    user = message.chat.id
    if prepare_tasks_doc(user) == 0:
        with open(f'{user}_tasks.xlsx', 'rb') as document:
            await bot.send_document(chat_id=user, document=document)
    else:
        await message.answer("Судя по моим данным, у вас еще не было активности.")


@dp.message_handler(lambda message: message.text == "Сколько я сегодня поработал?",
                    state=States.TASKS)
async def time_today_handler(message):
    user = message.chat.id
    time_today = get_working_time(user)
    await message.answer(f"Сегодня вы проработали {time_today[0]} часов {time_today[1]} минут")
