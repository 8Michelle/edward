# -*- coding: utf-8 -*-
"""This module contains handlers for tasks.

Task interface supports starting a new task and ending current one,
starting new session, checking today working time, current date and all data.
"""

from aiogram import types
import datetime

from core import dp, States, bot, KEYBOARDS
from tools import tasks
from tools.keyboard import make_keyboard


@dp.message_handler(lambda message: message.text == "Начать дело",
                    state=States.TASKS)
async def begin_task_handler(message):
    """Handle the start of a new task.

    Switches the state from TASKS to BEGIN_TASK.

    Creates begin task keyboard. Works with free task mode.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.BEGIN_TASK)

    buttons = list(tasks.get_tasks_list(user))
    buttons.append("Назад")

    await message.answer("Чем займетесь?",
                         reply_markup=make_keyboard(buttons))


@dp.message_handler(state=States.BEGIN_TASK)
async def begin_task_start_handler(message):
    """Handle the beginning of the new task with ``message`` name.

    Switches the state from BEGIN_TASK to TASKS.

    Creates busy task keyboard.

    """
    user = message.chat.id
    tasks.start_task(message.text, user)
    await dp.current_state(user=user).set_state(States.TASKS)

    message_text = f"Сейчас вы заняты: {message.text}"
    await message.answer(message_text,
                         reply_markup=make_keyboard(KEYBOARDS["busy_tasks"]))


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.BEGIN_TASK)
async def begin_task_revert_handler(message):
    """Handle a return to the tasks from the beginning a new task.

    Switches the state from BEGIN_TASK to TASKS.

    Creates free task keyboard.

    """
    await dp.current_state(user=message.chat.id).set_state(States.TASKS)
    await message.answer("Сейчас вы ничем не заняты",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Завершить",
                    state=States.TASKS)
async def end_task_handler(message):
    """Handle the end of the current task.

    Corresponds to the TASKS state.

    Creates free task keyboard. Works with busy task mode.

    """
    tasks.end_task(message.chat.id)

    await message.answer("Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Начать новую сессию",
                    state=States.TASKS)
async def new_session_handler(message):
    """Handle a new session starting.

    Switches the state from TASKS to NEW_SESSION.

    Creates new session keyboard. Works with free task mode.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.NEW_SESSION)

    date = datetime.date.today().isoformat()
    await message.answer(f"Новая дата {date.replace('-', '.')}?",
                         reply_markup=make_keyboard(KEYBOARDS["new_session"]))


@dp.message_handler(lambda message: message.text == "Все верно",
                    state=States.NEW_SESSION)
async def new_session_submit_handler(message):
    """Handle session date confirmation.

    Switches the state from NEW_SESSION to TASKS.

    Creates free task keyboard.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)

    date = datetime.date.today().isoformat()
    tasks.new_session(user=user, date=date)

    await message.answer("Начата новая сессия. Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(state=States.NEW_SESSION)
async def new_session_date_handler(message):
    """Handle the start of a new session with a custom date.

    Switches the state from NEW_SESSION to TASKS.

    Creates free tasks keyboard.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)

    tasks.new_session(user=user, date=message.text.replace('.', '-'))

    await message.answer(f"Начата новая сессия {message.text}. Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.NEW_SESSION)
async def new_session_revert_handler(message):
    """Handle a return to the tasks from the starting a new session.

    Switches the state from NEW_SESSION to TASKS.

    Creates free task keyboard.

    """
    await dp.current_state(user=message.chat.id).set_state(States.TASKS)

    await message.answer("Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Какое сегодня число?",
                    state=States.TASKS)
async def check_date_handler(message):
    """Answer a question about the current date.

    Corresponds to the TASKS state.

    Works with free mode.

    """
    user = message.chat.id
    date = tasks.check_date(user=user)
    message_text = f"Активная дата: {date}"
    # TODO: delete reply_markup
    await message.answer(message_text,
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Получить данные",
                    state=States.TASKS)
async def download_tasks_handler(message):
    """Handle a data request.

    Corresponds to the TASKS state.

    Sends a .xlsx data file. Works with free mode.

    """
    user = message.chat.id
    if tasks.prepare_tasks_doc(user) == 0:
        with open(f'{user}_tasks.xlsx', 'rb') as document:
            await bot.send_document(chat_id=user, document=document)

    else:
        await message.answer("Судя по моим данным, у вас еще не было активности.")


@dp.message_handler(lambda message: message.text == "Сколько я сегодня поработал?",
                    state=States.TASKS)
async def time_today_handler(message):
    """Handle a question of today working time.

    Corresponds to the TASKS state.

    Sends text message with today working time. Works with free mode.

    """
    user = message.chat.id
    time_today = tasks.get_working_time(user)
    await message.answer(f"Сегодня вы проработали {time_today[0]} часов {time_today[1]} минут")


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.TASKS)
async def tasks_revert_handler(message):
    """Handle a return to the skills from the tasks.

    Switches the state from TASKS to SKILLS.

    Creates skill keyboard. Works with both modes.

    """
    await dp.current_state(user=message.chat.id).set_state(States.SKILLS)

    await message.answer("Выберите функцию",
                         reply_markup=make_keyboard(KEYBOARDS["skills"]))
