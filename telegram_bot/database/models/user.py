from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

from telegram_bot.database.db_user_init import Base


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }


class User(MyBase):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    join_time: Mapped[datetime] = mapped_column(nullable=True)
    location: Mapped[int] = mapped_column(nullable=True)
    point: Mapped[str] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[bytes] = mapped_column(nullable=True)
    image_link: Mapped[str] = mapped_column(nullable=True)
