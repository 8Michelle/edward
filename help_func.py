from aiogram import types
from core import SKILLS
import json
import time
import datetime
import os


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


def create_tasks_file(user):
    filename = f'{user}_tasks.json'
    if filename not in os.listdir():
        with open(filename, 'w') as f:
            data = {'name': [], 'start': [], 'end': [], 'time': []}
            json.dump(data, f)


def start_task(name, user):
    filename = f'{user}_tasks.json'
    create_tasks_file(user)
    with open(filename, 'r') as f:
        data = json.load(f)
    data['name'].append(name)
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['start'].append(timestamp)
    with open(filename, 'w') as f:
        json.dump(data, f)


def get_data(user):
    create_tasks_file(user)
    with open(f'{user}_tasks.json', 'r') as f:
        data = json.load(f)
    return data


def end_task(user):
    filename = f'{user}_tasks.json'
    with open(filename, 'r') as f:
        data = json.load(f)
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    data['end'].append(timestamp)
    data['time'].append(timestamp - data['start'][-1])
    with open(filename, 'w') as f:
        json.dump(data, f)
