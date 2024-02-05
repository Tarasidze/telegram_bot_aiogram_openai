from datetime import datetime
from urllib.parse import urlparse

from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.utils.exceptions import BotBlocked

from telegram_bot.services.bot_start_button import keyboard_start, start_button
from telegram_bot.services.tele_bot_config import dp, bot
from telegram_bot.services.loger import log_on_startup, log_on_shutdown, log_open_ai_error
from telegram_bot.services.bot_location_button import keyboard_location, locations
from telegram_bot.services.openai_manager import send_request_to_ai

from telegram_bot.services.bot_point_button import (
    checklist_keyboard,
    short_check_list_options,
    checklist_options,
    comment_options,
    comment_keyboard,
)

from telegram_bot.database.database_manager import (
    add_user_id_to_database,
    add_location_and_point_to_db,
    add_comment_to_db,
    save_image_to_db,
    save_image_link_to_db,
    set_bot_blocked_db,
)
from telegram_bot.services.throttling import rate_limit


class UserChoice(StatesGroup):
    begin = State()
    location = State()
    point = State()
    photo_link = State()


@rate_limit(limit=3, key="/start")
@dp.message_handler(commands=["start", "help"],)
async def send_welcome(message: types.Message, state: FSMContext):
    """This handler will be called when client
     send `/start` or `/help` commands. and handle first menu level"""

    await state.reset_state()
    await UserChoice.location.set()

    await message.answer(
        "Привіт, Я телеграм бот! \n"
        "Я буду обробляти твої запити за допомогою OpenAI"
    )

    await message.answer("Виберіть локацію: ", reply_markup=keyboard_location)

    await add_user_id_to_database(
        user_id=message.from_user.id,
        date=datetime.now(),
        username=message.from_user.username
    )


@dp.message_handler()
async def reset_chat(message: types.Message, state: FSMContext):
    """The function will be called if the user wants to start from the beginning."""

    await message.answer(f"Бажаєте почати з початку?")
    await state.reset_state()
    await send_welcome(message, state)


@dp.message_handler(
    lambda message: message.text in locations,
    state=UserChoice.location
)
async def choose_location(message: types.Message, state: FSMContext):
    """The function handles the first-level menu."""

    location = message.text

    await message.answer(
        f"Ви обрали {location}. Тепер виберіть пункт:",
        reply_markup=checklist_keyboard
    )

    await UserChoice.point.set()
    await state.update_data(location=location)


@dp.message_handler(state=UserChoice.location)
async def get_location_first(message: types.Message):
    """The function calls when a user tries to type instead of pressing button."""

    await message.answer(
        f"Будь ласка, спочатку оберіть локацію",
        reply_markup=keyboard_location
    )


@dp.message_handler(
    lambda message: message.text in checklist_options,
    state=UserChoice.point
)
async def handle_poit(message: types.Message, state: FSMContext):
    """The function handles second-level menu, saves to database."""

    option = message.text

    await state.update_data(point=option)

    if option in short_check_list_options:
        await message.answer(
            f"Ви обрали '{option}'. Дякую за надану інформацію",
            reply_markup=keyboard_start
        )
        user_data = await state.get_data()

        await add_location_and_point_to_db(
            user_id=message.from_user.id,
            location=user_data.get("location"),
            point=user_data.get("point")
        )

        await state.reset_state()

    elif option in comment_options:

        await message.answer(
            f"Ви обрали '{option}'. Очікую на коментар",
            reply_markup=comment_keyboard
        )


@dp.message_handler(state=UserChoice.point)
async def user_comment(message: types.Message, state: FSMContext):
    """The function handles user comment passes them to Openai and sends answear."""

    user_data = await state.get_data()

    await add_comment_to_db(
        user_id=message.from_user.id,
        comment=message.text,
        location=user_data.get("location"),
        point=user_data.get("point")
    )

    await message.answer(
        f"Зачекайте на відповідь gомічника на основі ШІ.\n "
        f"Також Ви можете добавити фото(jpg, png), посилання на зображення, \n"
        f"або повернутись на початок",
        reply_markup=keyboard_start)
    try:
        await message.answer(
            await send_request_to_ai(
                location=user_data.get("location"),
                message=message.text
            )
        )
    except Exception as e:
        await log_open_ai_error(e.__str__())

    await message.answer(
        "Бажаєте додати посилання або фото?",
        reply_markup=keyboard_start)

    await UserChoice.photo_link.set()


@dp.message_handler(state=UserChoice.photo_link)
async def user_link(message: types.Message, state: FSMContext):
    """The function handles the user link and saves it to the database."""

    if message.text in start_button:
        await reset_chat(message, state)
        return

    if message.text:
        link = message.text
        parsed_url = urlparse(link)

        if parsed_url.scheme and parsed_url.netloc:
            await save_image_link_to_db(
                user_id=message.from_user.id,
                image_link=link,
            )
            await message.answer("Дякую з посилння!")
            await state.reset_state()

        else:
            await message.answer(
                f"Невалідне посилання, спробуйте ще раз"
            )
            await UserChoice.photo_link.set()


@dp.message_handler(
    content_types=ContentType.PHOTO,
    state=UserChoice.photo_link
)
async def user_photo(message: types.Message):
    """The function handles the user photo and saves it to the database."""

    if message.photo:
        photo_id = message.photo[-1].file_id
        file = await bot.download_file_by_id(photo_id)
        photo_data = file.read()

        await save_image_to_db(
            user_id=message.from_user.id,
            image=photo_data,
        )

        await message.answer("Дякую за фото!")


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked, state: FSMContext) -> bool:
    ser_id = state.user
    await set_bot_blocked_db(user_id=ser_id, status="blocked")


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=log_on_startup,
        on_shutdown=log_on_shutdown,
        skip_updates=True
    )
