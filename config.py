from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = config('TOKEN')

bot = Bot(token=TOKEN)
storage=MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

staff = [6896900558, 2091942960, 5649689334]