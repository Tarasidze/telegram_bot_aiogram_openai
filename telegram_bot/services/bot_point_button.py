from aiogram import types


checklist_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    selective=True
)
checklist_options = [
    "Пункт 1",
    "Пункт 2",
    "Пункт 3",
    "Пункт 4",
    "Пункт 5",
    "Все чисто",
    "Залишити коментар",
]
checklist_keyboard.add(*checklist_options)


short_check_list_options = [
    "Пункт 1",
    "Пункт 2",
    "Пункт 3",
    "Пункт 4",
    "Пункт 5",
    "Все чисто",
]


comment_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    selective=True
)
comment_options = [
    "Залишити коментар",
]
comment_keyboard.add(*comment_options)
