import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import json
import time
import datetime


logging.basicConfig(level=logging.INFO)

bot = Bot(token="1197211678:AAFMXwjRZIyoCWc8qLvUPcq31t5hcCGG9Fk")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class States(StatesGroup):
    S_START = State()
    S_CHOOSE_SKILL = State()
    S_TASKS = State()

SKILLS = ['Дела'] # организовать хранение данных

def make_start_keyword():
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Что ты умеешь?"))
    poll_keyboard.add(types.KeyboardButton(text="Кто тебя создал?"))
    poll_keyboard.add(types.KeyboardButton(text="Функции"))
    return poll_keyboard

def make_skills_keyboard():
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for skill in SKILLS:
        poll_keyboard.add(types.KeyboardButton(text=skill))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    return poll_keyboard

def start_task(name):
    with open('tasks.json', 'r') as f:
        data = json.load(f)
    data['name'].append(name)
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['start'].append(timestamp)
    with open('tasks.json', 'w') as f:
        json.dump(data, f)

def get_data():
    with open('tasks.json', 'r') as f:
        data = json.load(f)
    return data

def end_task():
    with open('tasks.json', 'r') as f:
        data = json.load(f)
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['end'].append(timestamp)
    data['time'].append(timestamp - data['start'][-1])
    with open('tasks.json', 'w') as f:
        json.dump(data, f)


@dp.message_handler(commands=['start'])
async def start(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.S_START)
    await message.answer("Привет! Меня зовут Эдвард", reply_markup=make_start_keyword())

@dp.message_handler(lambda message: message.text == "Что ты умеешь?", state=States.S_START)
async def skills_about(message):
    answer = """Пока не очень многое. Но Создатель работает над расширением моего\
    функционала. Если у вас есть предложения, то Он всегда готов их выслушать.\
    Чтобы посмотреть функционал, доступный в данный момент, нажмите 'Функции'."""
    await message.answer(answer)

@dp.message_handler(lambda message: message.text == "Кто тебя создал?", state=States.S_START)
async def creator(message):
    answer = "Михаил Коновалов"
    await message.answer(answer)

@dp.message_handler(lambda message: message.text == "Функции", state=States.S_START)
async def skills(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.S_CHOOSE_SKILL)
    await message.answer("Выберите интересующую функцию", reply_markup=make_skills_keyboard())

@dp.message_handler(lambda message: message.text == "Назад", state=States.S_CHOOSE_SKILL)
async def revert_1(message):
    await dp.current_state(user=message.chat.id).set_state(States.S_START)
    await message.answer("Привет! Меня зовут Эдвард", reply_markup=make_start_keyword())

@dp.message_handler(lambda message: message.text == "Дела", state=States.S_CHOOSE_SKILL)
async def tasks(message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(States.S_TASKS)
    data = get_data()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(data['name']) == len(data['end']):
        message_text = "Чем займетесь?"
    else:
        message_text = f"Сейчас вы заняты: {data['name'][-1]}"
        poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer(message_text, reply_markup=poll_keyboard)

@dp.message_handler(lambda message: message.text == "Завершить", state=States.S_TASKS)
async def stop_task(message):
    end_task()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer("Чем займетесь?", reply_markup=poll_keyboard)

@dp.message_handler(lambda message: message.text == "Назад", state=States.S_TASKS)
async def revert_to_skills(message):
    await dp.current_state(user=message.chat.id).set_state(States.S_CHOOSE_SKILL)
    await message.answer("Выберите интересующую функцию", reply_markup=make_skills_keyboard())

@dp.message_handler(state=States.S_TASKS)
async def create_task(message):
    start_task(message.text)
    data = get_data()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    message_text = f"Сейчас вы заняты: {data['name'][-1]}"
    await message.answer(message_text, reply_markup=poll_keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
