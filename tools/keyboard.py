# -*- coding: utf-8 -*-
from aiogram import types


def make_keyboard(buttons):
    """Creates a bot keyboard with ``buttons``.

    Args:
        buttons (list): list of strings.

    Returns:
        types.ReplyKeyboardMarkup: keyboard with ``buttons``.

    """
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for button_text in buttons:
        poll_keyboard.add(types.KeyboardButton(text=button_text))

    return poll_keyboard
