from aiogram import types
from core import SKILLS
import json
import time
import datetime
import os
from collections import defaultdict
import pandas as pd


def make_start_keyboard():
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


def make_tasks_keyboard():
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Начать дело"))
    poll_keyboard.add(types.KeyboardButton(text="Начать новую сессию"))
    poll_keyboard.add(types.KeyboardButton(text="Сколько я сегодня поработал?"))
    poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
    # poll_keyboard.add(types.KeyboardButton(text="Построить график"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    return poll_keyboard


def make_new_session_keyboard():
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Все верно"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    return poll_keyboard


def make_busy_keyboard():
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    return poll_keyboard


def make_begin_task_keyboard(user):
    filename = f'{user}_tasks.json'
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    if filename in os.listdir():
        with open(f"{user}_tasks.json") as f:
            data = json.load(f)
        names = set()
        for name in data["name"][::-1]:
            if len(names) < 5:
                names.add(name)
            else:
                break
        for name in names:
            poll_keyboard.add(types.KeyboardButton(text=name))

    return poll_keyboard


#-----------------Обработчики--------------------

# user_tasks.json - списки названий, времен начала, окончания и длительности дел
# user_tasks_s.json - матрица дела-дни, содержит время занятия определнным делом в определенный день


def start_task(name, user): # фиксирует в файле user_tasks.json название дела и время начала
    filename = f'{user}_tasks.json'
    if filename not in os.listdir():
        data = {
            'name': [],
            'start': [],
            'end': [],
            'time': []
        }
    else:
        with open(filename, 'r') as f:
            data = json.load(f)

    data['name'].append(name)
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['start'].append(timestamp)
    with open(filename, 'w') as f:
        json.dump(data, f)


def end_task(user):

    # извлекаем список всех дел
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    filename = f'{user}_tasks.json'
    with open(filename, 'r') as f:
        data = json.load(f)

    # находим в нем последнее дело, закрываем его end, считаем интервал,
    # запоминаем имя и пишем обратно в файл. Больше data не меняется.
    name = data["name"][-1]
    time_int = timestamp - data['start'][-1]
    data['end'].append(timestamp)
    data['time'].append(time_int)
    with open(filename, 'w') as f:
        json.dump(data, f)

    # извлекаем файл с матрицей. Предварительный вызов new_session гарантирует его наличие
    filename_s = f'{user}_tasks_s.json'
    with open(filename_s, 'r') as f:
        data_s = json.load(f)
    date = max(data_s)

    if name in data_s[date]:
        data_s[date][name] += time_int
    else:
        data_s[date][name] = time_int
    with open(filename_s, 'w') as f:
        json.dump(data_s, f)


def new_session(user, date): # добавляет новую дневную запись в файл user_tasks_s.json

    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        data_s = {
            date: defaultdict(int)
        }
    else:
        with open(filename_s, 'r') as f:
            data_s = json.load(f)
            data_s[date] = defaultdict(int)

    with open(filename_s, 'w') as f:
        json.dump(data_s, f)


#-------------------Обработка данных----------------------

def prepare_tasks_doc(user):
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        return 1
    with open(filename_s, 'r') as f:
        data_s = json.load(f)

    df = pd.DataFrame(data_s).T.fillna(0)
    df['sum'] = df.sum(axis=1)
    for column in df.columns:
        df[column] = pd.to_datetime(df[column], unit='s')
    df -= pd.to_datetime(0)
    df.to_excel(f'{user}_tasks.xlsx', index=True)

    return 0


def get_working_time(user):
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        return "00:00:00"

    with open(filename_s, 'r') as f:
        data_s = json.load(f)
    df = pd.DataFrame(data_s).T.fillna(0)
    df['sum'] = df.sum(axis=1)
    for column in df.columns:
        df[column] = pd.to_datetime(df[column], unit='s')
    df -= pd.to_datetime(0)
    df.sort_index()

    return str(df.iloc[-1, :]['sum']).split()[-1].split(':')[:-1]