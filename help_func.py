from aiogram import types
from core import SKILLS
import json
import time
import datetime
import os
from collections import defaultdict
import pandas as pd


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


def start_task(name, user):
    filename = f'{user}_tasks.json'
    if filename not in os.listdir():
        data = {'name': [],
                'start': [],
                'end': [],
                'time': []}
    else:
        with open(filename, 'r') as f:
            data = json.load(f)

    data['name'].append(name)
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['start'].append(timestamp)
    with open(filename, 'w') as f:
        json.dump(data, f)


def new_session(user):
    new_date = datetime.date.today().isoformat()
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        data_s = {
            "date": new_date,
            new_date: defaultdict(int)
        }
    else:
        with open(filename_s, 'r') as f:
            data_s = json.load(f)

    data_s['date'] = new_date
    data_s[new_date] = defaultdict(int)

    with open(filename_s, 'w') as f:
        json.dump(data_s, f)


def end_task(user):
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        date = datetime.date.today().isoformat()
        data_s = {
            "date": date,
            date: defaultdict(int)
        }
    else:
        with open(filename_s, 'r') as f:
            data_s = json.load(f)
        date = data_s['date']

    filename = f'{user}_tasks.json'
    with open(filename, 'r') as f:
        data = json.load(f)

    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['end'].append(timestamp)
    data['time'].append(timestamp - data['start'][-1])
    with open(filename, 'w') as f:
        json.dump(data, f)

    name = data['name'][-1]
    time_int = data['time'][-1]
    # print(name, date)
    if name in data_s[date]:
        data_s[date][name] += time_int
    else:
        data_s[date][name] = time_int
    with open(filename_s, 'w') as f:
        json.dump(data_s, f)


def prepare_tasks_doc(user):
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        return 1
    with open(filename_s, 'r') as f:
        data_s = json.load(f)

    data_s.pop("date")
    df = pd.DataFrame(data_s).T.fillna(0)
    df['sum'] = df.sum(axis=1)
    for column in df.columns:
        df[column] = pd.to_datetime(df[column], unit='s')
    df -= pd.to_datetime(0)
    df.to_excel(f'{user}_tasks.xlsx', index=True)
    return 0