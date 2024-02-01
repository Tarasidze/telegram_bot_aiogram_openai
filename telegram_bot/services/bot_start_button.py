from aiogram import types


keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
start_button = ["Початок"]
keyboard_start.add(*start_button)
