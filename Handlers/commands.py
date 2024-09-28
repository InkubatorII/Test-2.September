from aiogram import types, Dispatcher
import os

from config import bot


# Запуск бота
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Добро пожаловать в нашего бота!',
                           reply_markup=start)

async def info_command(message: types.Message):
    await message.answer("Этот бот предназначен для управления товарами и заказами.")

def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_command, commands=['info'])