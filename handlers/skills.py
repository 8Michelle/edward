from aiogram import types
from core import dp, States
from help_func import make_start_keyword, get_data, create_tasks_file


@dp.message_handler(lambda message: message.text == "Назад", state=States.S_CHOOSE_SKILL)
async def revert_1(message):
    await dp.current_state(user=message.chat.id).set_state(States.S_START)
    await message.answer("Привет! Меня зовут Эдвард", reply_markup=make_start_keyword())


@dp.message_handler(lambda message: message.text == "Дела", state=States.S_CHOOSE_SKILL)
async def tasks(message):
    user = message.chat.id
    state = dp.current_state(user=user)
    await state.set_state(States.S_TASKS)
    data = get_data(user)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(data['name']) == len(data['end']):
        poll_keyboard.add(types.KeyboardButton(text="Получить данные"))
        message_text = "Чем займетесь?"
    else:
        message_text = f"Сейчас вы заняты: {data['name'][-1]}"
        poll_keyboard.add(types.KeyboardButton(text="Завершить"))
    poll_keyboard.add(types.KeyboardButton(text="Назад"))
    await message.answer(message_text, reply_markup=poll_keyboard)
