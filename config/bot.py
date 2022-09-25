import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


class LangState(StatesGroup):
    """Класс описывает state 'lang' в который будем записывать выбранный пользователем язык документа"""

    lang = State()
