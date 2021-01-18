# -*- coding: utf-8 -*-
from aiogram import types
from core import dp, States, bot, KEYBOARDS
# from tools import make_keyboard, get_tasks_list, end_task, start_task,\
#     new_session, prepare_tasks_doc, get_working_time, check_date
from tools import tasks
from tools.keyboard import make_keyboard
import datetime


@dp.message_handler(lambda message: message.text == "Завершить",
                    state=States.TASKS)
async def end_task_handler(message):
    """Handles stop message. Creates tasks keyboard.
    Using with busy mode.
    Corresponds to the TASKS state.
    Allows to go to task functions.

    Args:
        message (types.message.Message): stop task message.

    """
    tasks.end_task(message.chat.id)

    await message.answer("Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.TASKS)
async def tasks_revert_handler(message):
    """Handles returning to the SKILLS state.
    Creates a skills keyboard.
    Corresponds to the TASKS state.
    Allows to go to all the bot skills.

    Args:
        message (types.message.Message): returning message.

    """
    await dp.current_state(user=message.chat.id).set_state(States.SKILLS)

    await message.answer("Выберите функцию",
                         reply_markup=make_keyboard(KEYBOARDS["skills"]))


@dp.message_handler(lambda message: message.text == "Начать новую сессию",
                    state=States.TASKS)
async def new_session_handler(message):
    """Handles a new session message.
    Starts a date check. switches the state to NEW_SESSION.
    Creates a new session keyboard.
    You can choose new session with automatically set date or with custom date.

    Args:
        message (types.message.Message): new session message.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.NEW_SESSION)

    date = datetime.date.today().isoformat()
    await message.answer(f"Новая дата {date.replace('-', '.')}?",
                         reply_markup=make_keyboard(KEYBOARDS["new_session"]))


@dp.message_handler(lambda message: message.text == "Все верно",
                    state=States.NEW_SESSION)
async def new_session_submit_handler(message):
    """Handles confirmation of a new session date.
    Switches the state to TASKS. Starts new session.
    Creates tasks keyboard. Allows to go to task functions.

    Args:
        message (types.message.Message): new session confirmation message.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)

    date = datetime.date.today().isoformat()
    tasks.new_session(user=user, date=date)

    await message.answer("Начата новая сессия. Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Назад",
                    state=States.NEW_SESSION)
async def new_session_revert_handler(message):
    """Handles returning to the TASKS state.
    Corresponds to the NEW_SESSION state.
    Switches the state to TASKS.
    Creates tasks keyboard. Allows to go to task functions.

    Args:
        message (types.message.Message): tasks returning message.

    """
    await dp.current_state(user=message.chat.id).set_state(States.TASKS)

    await message.answer("Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(state=States.NEW_SESSION)
async def new_session_date_handler(message):
    """Handles message with custom session date.
    Switches the state to TASKS. Creates tasks keyboard.
    Allows to go to task functions.

    Args:
        message (types.message.Message): custom date message.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.TASKS)

    tasks.new_session(user=user, date=message.text.replace('.', '-'))

    await message.answer(f"Начата новая сессия {message.text}. Сейчас вы ничем не заняты.",
                         reply_markup=make_keyboard(KEYBOARDS["free_tasks"]))


@dp.message_handler(lambda message: message.text == "Начать дело", state=States.TASKS)
async def begin_task_handler(message):
    """Handles starting a new task.
    Switches the state to BEGIN_TASK.
    Creates begin tasks keyboard.

    Args:
        message (types.message.Message): new task message.

    """
    user = message.chat.id
    await dp.current_state(user=user).set_state(States.BEGIN_TASK)

    buttons = list(tasks.get_tasks_list(user))
    buttons.append("Назад")

    await message.answer("Чем займетесь?",
                         reply_markup=make_keyboard(buttons))


@dp.message_handler(lambda message: message.text == "Назад", state=States.BEGIN_TASK)
async def begin_task_revert_handler(message):
    """Handles returning to the TASKS state from starting new task.
    Switches the state to TASKS. Creates tasks keyboard.

    Args:
        message (types.message.Message): returning message.

    """
    await dp.current_state(user=message.chat.id).set_state(States.TASKS)
    await message.answer("Сейчас вы ничем не заняты",
                         reply_markup=make_keyboard(KEYBOARDS["tasks"]))


@dp.message_handler(state=States.BEGIN_TASK)
async def begin_task_start_handler(message):
    """Handles new task beginning.
    Switches the state to TASKS.
    Creates busy keyboard.

    Args:
        message (types.message.Message): message with new task name.

    """
    user = message.chat.id
    tasks.start_task(message.text, user)
    await dp.current_state(user=user).set_state(States.TASKS)

    message_text = f"Сейчас вы заняты: {message.text}"
    await message.answer(message_text,
                         reply_markup=make_keyboard(KEYBOARDS["busy_tasks"]))


@dp.message_handler(lambda message: message.text == "Какое сегодня число?",
                    state=States.TASKS)
async def check_date_handler(message):
    """Handles a date request.

    Args:
        message (types.message.Message): message with date request.

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
    """Handles data request.
    Sends .xlsx document with tasks data.

    Args:
        message (types.message.Message): message with data request.

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
    """Handles today's working time request.

    Args:
        message (types.message.Message): message with today's working time request.

    """
    user = message.chat.id
    time_today = tasks.get_working_time(user)
    await message.answer(f"Сегодня вы проработали {time_today[0]} часов {time_today[1]} минут")
