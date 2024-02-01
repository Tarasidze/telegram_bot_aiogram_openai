from aiogram import types


keyboard_location = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
locations = ["Локація 1", "Локація 2", "Локація 3", "Локація 4", "Локація 5"]
keyboard_location.add(*locations)
