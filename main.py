import asyncio
import logging
from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
from handlers import music

# Загружаем переменные из .env
load_dotenv()

async def main():
    # Настраиваем логи, чтобы видеть ошибки в консоли
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Подключаем наш обработчик музыки
    dp.include_router(music.router)

    print("🚀 MusicBot запущен на Linux!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")