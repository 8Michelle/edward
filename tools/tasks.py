# -*- coding: utf-8 -*-
"""This module contains functions for working with tasks and their files."""

import json
import time
import datetime
import os
from collections import defaultdict
import pandas as pd


def get_tasks_list(user):
    """Reads the last 5 tasks from the .join file for ``user``.

    Args:
        user (int): user id.

    Returns:
        set: set of 5 last tasks for ``user``.

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
    """Starts new task with ``name`` for ``user``.

    Reads or creates user .json file with tasks.
    Adds a new task and its start time.

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
    """Ends the current task for ``user``.

    Reads user .json file with tasks, checks last task, sets end time and duration.
    Increments duration of this task in .json file with matrix.

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
    """Starts new session for ``user`` with ``date``.

    Reads or creates a matrix file for ``user``.
    Adds new entry with ``date``.

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
    """Reads the current date for ``user``.

    Reads the matrix file and takes the last entry date.

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
    """Prepares .xlsx doc from the .json matrix file for ``user`` with all tasks.

    Creates pandas dataframe from a .json matrix file and loads it into a .xlsx file.

    Args:
        user (int): user id.

    Returns:
        int: code of the answer (0 if OK, 1 if ``user`` file doesn't exist).

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
    """Reads and sums last matrix file entry for ``user``.

    Args:
        user (int): user id.

    Returns:
        list: list of strings inn format ["HH", "MM"].

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
