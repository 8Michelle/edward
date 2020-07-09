from aiogram import types
from core import dp, States, bot, TOKEN
from help_func import end_task, start_task, make_skills_keyboard,\
    new_session, prepare_tasks_doc, make_tasks_keyboard
import pandas as pd


@dp.message_handler(lambda message: message.text == "Завершить", state=States.S_TASKS)
async def end_task_handler(message):
    end_task(message.chat.id)
    # poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
    # poll_keyboard.add(types.KeyboardButton(text="Начать новую сессию"))
    # poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer("Чем хотите заняться?", reply_markup=make_tasks_keyboard())


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
    if new_session(user) == 1:
        message_text = "День еще не закончился. Для начала дела введите его название"
    else:
        message_text = "Начата новая сессия. Чем хотите заняться?"
    # poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
    # poll_keyboard.add(types.KeyboardButton(text="Начать новую сессию"))
    # poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer(message_text,
                         reply_markup=make_tasks_keyboard())


@dp.message_handler(lambda message: message.text == "Сколько я сегодня поработал?",
                    state=States.S_TASKS)
async def time_today_handler(message):
    user = message.chat.id
    if prepare_tasks_doc(user) == 1:
        await message.answer("Судя по моим данным, у вас еще не было активности.")
    else:
        df = pd.read_csv(f"{user}_tasks.csv")
        time_today = str(df.iloc[-1, :]['sum']).split()[-1].split(':')[:-1]
        await message.answer(f"Сегодня вы проработали {time_today[0]} часов {time_today[1]} минут")


@dp.message_handler(state=States.S_TASKS)
async def start_task_handler(message):
    user = message.chat.id
    start_task(message.text, user)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    message_text = f"Сейчас вы заняты: {message.text}"
    await message.answer(message_text, reply_markup=poll_keyboard)
