# -*- coding: utf-8 -*-
"""This module contains functions for working with tasks and their files."""

import json
import time
import datetime
import os
from collections import defaultdict
import pandas as pd


def check_busy(user):
    """Check task mode for ``user``, return 0 if free, 1 if busy,
    -1 if there is task error.

    Reads ``user`` task file.

    Args:
        user (int): user id.

    Returns:
        int: answer code.

    """
    filename = f'{user}_tasks.json'
    if filename not in os.listdir():
        return 0

    else:
        with open(filename, 'r') as f:
            data = json.load(f)

        if len(data['name']) < len(data['end']):
            return -1

        if len(data['name']) > len(data['end']):
            return 1

        return 0


def get_tasks_list(user):
    """Return the last 5 tasks for ``user``.

    Reads .json tasks file.

    Args:
        user (int): user id.

    Returns:
        set: set of 5 strings.

    """
    filename = f'{user}_tasks.json'

    tasks = set()
    if filename in os.listdir():
        with open(f"{user}_tasks.json") as f:
            data = json.load(f)

        for name in data["name"][::-1]:
            if len(tasks) < 5:
                tasks.add(name)
            else:
                break

    return tasks


def start_task(name, user):
    """Start new task with ``name`` for ``user``.

    Updates .json file with tasks.

    Args:
        name (str): name of the task to start.
        user (int): user id.

    """
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
    """End the current task for ``user``.

    Updates .json file with matrix and file with tasks.

    Args:
        user (int): user id.

    """

    timestamp = time.mktime(datetime.datetime.now().timetuple())
    filename = f'{user}_tasks.json'
    with open(filename, 'r') as f:
        data = json.load(f)

    name = data["name"][-1]
    time_int = timestamp - data['start'][-1]
    data['end'].append(timestamp)
    data['time'].append(time_int)
    with open(filename, 'w') as f:
        json.dump(data, f)

    # TODO: Check for a matrix file.
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


def new_session(user, date):
    """Start new session for ``user`` with ``date``.

    Updates a matrix file for ``user``.

    Args:
        user (int): user id.
        date (str): date in format YYYY-MM-DD.

    """

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


def check_date(user):
    """Return the current date for ``user``.

    Reads the last date from the user matrix file.

    Args:
        user (int): user id.

    Returns:
        str: date in format YYYY-MM-DD.

    """

    filename_s = f"{user}_tasks_s.json"
    if filename_s not in os.listdir():
        return
    else:
        with open(filename_s, 'r') as f:
            data_s = json.load(f)

    date = max(data_s)
    return date


def prepare_tasks_doc(user):
    """Convert the .json matrix file to .xlsx doc for ``user``.

    Args:
        user (int): user id.

    Returns:
        int: code of the answer (0 if OK, 1 if ``user`` matrix file doesn't exist).

    """
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        return 1
    with open(filename_s, 'r') as f:
        data_s = json.load(f)

    df = pd.DataFrame(data_s).T.fillna(0)
    df['sum'] = df.sum(axis=1)
    for column in df.columns:
        df[column] = pd.to_datetime(df[column], unit='s')

    df -= pd.to_datetime(0)  # Reduction from UNIX time to duration.
    df.to_excel(f'{user}_tasks.xlsx')

    return 0


def get_working_time(user):
    """Return today working time for ``user``.

    Reads the last entry from matrix .json file.

    Args:
        user (int): user id.

    Returns:
        list: list of strings in format ["HH", "MM"].

    """
    filename_s = f'{user}_tasks_s.json'
    if filename_s not in os.listdir():
        return ["00", "00"]

    with open(filename_s, 'r') as f:
        data_s = json.load(f)
    df = pd.DataFrame(data_s).T.fillna(0)

    df['sum'] = df.sum(axis=1)

    for column in df.columns:
        df[column] = pd.to_datetime(df[column], unit='s')
    df -= pd.to_datetime(0)
    df.sort_index()

    # Sums all columns in the last row, split timedelta like string and get HH and MM.
    return str(df.iloc[-1, :]['sum']).split()[-1].split(':')[:-1]
