import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import CommandStart

# 🧩 Встав сюди свій новий токен
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Не знайдено TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):

    # Створюємо кнопки меню
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Переглянути каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="🎯 Підібрати авто", callback_data="select")],
        [InlineKeyboardButton(text="🔥 Акції та знижки", callback_data="sales")],
        [InlineKeyboardButton(text="📞 Зв'язок з менеджером", callback_data="manager")]
    ])

    # Локальне фото
    photo_file = FSInputFile("Photo.jpg")

    # Відправка фото з текстом та кнопками
    await message.answer_photo(
        photo=photo_file,
        caption="🚗 <b>KidsRide</b>\n\nПривіт! Обери дію нижче 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
