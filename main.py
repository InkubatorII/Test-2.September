import logging
from aiogram.utils import executor
from config import bot, dp, staff
from Handlers import commands, fsm_store, send_products, fsm_order
from db import db_main
from aiogram.utils.exceptions import BotBlocked

async def on_startup(dp):
    try:
        await bot.send_message(chat_id=6896900558, text="Добро пожаловать в нашего бота!")
    except BotBlocked:
        print("Бот был заблокирован пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

fsm_store.register_store(dp)
commands.register_commands(dp)
send_products.register_send_products_handler(dp)
fsm_order.register_order_handler(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)