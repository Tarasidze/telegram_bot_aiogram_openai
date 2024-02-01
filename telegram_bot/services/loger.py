import sys
import datetime
import logging

from telegram_bot.services.tele_bot_config import dp


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("bot_logs.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


async def log_on_startup(dp):
    logging.info(
            f"Time: {datetime.datetime.now()},"
            f"Bot has started"
        )


async def log_on_shutdown(dp):
    logging.info(
            f"Time: {datetime.datetime.now()},"
            f"Bot has end"
        )
