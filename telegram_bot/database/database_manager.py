from datetime import datetime
from sqlalchemy import desc
from telegram_bot.database.models.user import User
from telegram_bot.database.db_user_init import db


async def add_user_id_to_database(
        user_id: int,
        date: datetime,
        username: str = None
) -> None:

    new_user = User(user_id=user_id, join_time=date, username=username)
    db.add(new_user)
    db.commit()


async def add_location_and_point_to_db(
        user_id: int,
        location: str,
        point: str
) -> bool:

    user = db.query(User).filter_by(user_id=user_id).order_by(desc(User.join_time)).first()

    if user:
        user.location = location
        user.point = point
        db.commit()
        return True

    return False


async def add_comment_to_db(
        user_id: int,
        comment: str,
        location: str,
        point: str
) -> bool:

    user = db.query(User).filter_by(user_id=user_id).order_by(desc(User.join_time)).first()

    if user:
        user.comment = comment
        user.location = location
        user.point = point
        db.commit()
        return True

    return False


async def save_image_to_db(user_id: int, image: bytes) -> bool:
    user = db.query(User).filter_by(user_id=user_id).order_by(desc(User.join_time)).first()

    if user:
        user.image = image
        db.commit()
        return True

    return False


async def save_image_link_to_db(user_id: int, image_link: bytes) -> bool:
    user = db.query(User).filter_by(user_id=user_id).order_by(desc(User.join_time)).first()

    if user:
        user.image_link = image_link
        db.commit()
        return True

    return False


async def set_bot_blocked_db(user_id: int, status: str) -> bool:
    user = db.query(User).filter_by(user_id=user_id).order_by(desc(User.join_time)).first()

    if user:
        user.status = status
        db.commit()
        return True

    return False
