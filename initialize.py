from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

storage_m = MemoryStorage()

bot = Bot(token=os.getenv('MY_TOKEN'),
          parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage_m)