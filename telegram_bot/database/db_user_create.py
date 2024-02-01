from telegram_bot.database.db_user_init import Base, engine

from telegram_bot.database.models.user import User


def create_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
