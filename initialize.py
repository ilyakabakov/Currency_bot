from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
storage_m = MemoryStorage()

bot = Bot(token=os.getenv('MY_TOKEN'))
dp = Dispatcher(bot, storage=storage_m)