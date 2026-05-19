from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.downloader import search_tracks, download_by_url
import os
import asyncio

router = Router()

# Приветствие по команде /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}! 🎧\nОтправь мне название песни, и я найду варианты!")

# Поиск и выдача списка кнопками
@router.message(F.text)
async def handle_search(message: types.Message):
    if message.text.startswith('/'): return
    
    status_msg = await message.answer("🔍 Ищу варианты...")
    results = await asyncio.to_thread(search_tracks, message.text)
    
    if not results:
        return await status_msg.edit_text("Ничего не нашел. попробуй по-другому.")

    builder = InlineKeyboardBuilder()
    for i, track in enumerate(results):
        # В callback_data зашиваем индекс или часть URL (лимит 64 символа!)
        # Для простоты используем короткий ID видео из ссылки
        video_id = track['url'].split('=')[-1]
        builder.row(types.InlineKeyboardButton(
            text=f"⬇️ {track['title'][:40]}...", 
            callback_data=f"dl_{video_id}")
        )

    await status_msg.edit_text("Выбери нужный трек:", reply_markup=builder.as_markup())

# Обработка нажатия на кнопку (Скачивание)
@router.callback_query(F.data.startswith("dl_"))
async def handle_download(callback: types.Callback_query):
    video_id = callback.data.split('_')[1]
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    await callback.answer("Начинаю загрузку... ⏳")
    wait_msg = await callback.message.answer("📥 Скачиваю и конвертирую...")
    
    try:
        file_path, title = await asyncio.to_thread(download_by_url, url)
        audio = types.FSInputFile(file_path)
        
        await callback.message.answer_audio(audio=audio, caption=f"Готово: {title}")
        if os.path.exists(file_path): os.remove(file_path)
        await wait_msg.delete()
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")
