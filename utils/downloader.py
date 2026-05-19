import yt_dlp
import os
import asyncio

# Функция только для поиска списка песен
def search_tracks(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch5:', # Ищем 5 вариантов
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        results = []
        for entry in info['entries']:
            results.append({
                'title': entry.get('title'),
                'url': entry.get('webpage_url'),
                'duration': entry.get('duration')
            })
        return results

# Функция только для скачивания конкретной ссылки
def download_by_url(url):
    download_path = 'downloads'
    if not os.path.exists(download_path): os.makedirs(download_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        return file_path, info.get('title')
