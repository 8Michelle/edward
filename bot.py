# -*- coding: utf-8 -*-
"""This code starts the bot."""

from aiogram import executor

from core import dp
import handlers


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
