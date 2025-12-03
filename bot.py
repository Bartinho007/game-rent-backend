import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from db import SessionLocal
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types.web_app_info import WebAppInfo
from config import API_URL  # если хочешь, можно вынести URL в конфиг

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Каталог оборудования")],
            [KeyboardButton(text="🛒 Мои заказы"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )

    # webapp_kb = InlineKeyboardMarkup(inline_keyboard=[
    #     [InlineKeyboardButton(text="Открыть каталог", web_app=WebAppInfo(url=API_URL))]
    # ])

    await message.answer(
        "🎮 Добро пожаловать в аренду игрового оборудования!\n\n"
        "Нажми кнопку ниже, чтобы открыть каталог.",
        # reply_markup=webapp_kb
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
