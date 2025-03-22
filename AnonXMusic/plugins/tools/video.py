import os
import shutil
import asyncio
from re import findall
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from AnonXMusic import app

DOWNLOAD_DIR = "downloads"

YTDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
}


@app.on_message(filters.command(["vid", "video"], prefixes=["/", "!"]))
async def video_search(client: Client, message: Message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Please provide a search query.")

    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "")
    except IndexError:
        lim = 2  # Default limit

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    msg = await message.reply("Searching videos...")

    search_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
        'force_generic_extractor': False,
    }

    try:
        with YoutubeDL(search_opts) as ydl:
            results = ydl.extract_info(f"ytsearch{lim}:{query}", download=False)
            videos = results.get("entries", [])
            if not videos:
                return await msg.edit("No videos found.")

        downloaded_files = []

        for i, vid in enumerate(videos[:lim]):
            url = vid.get("url")
            title = vid.get("title")
            await msg.edit(f"Downloading: {title}")
            try:
                with YoutubeDL(YTDL_OPTIONS) as ydl:
                    info = ydl.extract_info(f"https://www.youtube.com/watch?v={url}", download=True)
                    filepath = ydl.prepare_filename(info).replace(".webm", ".mp4").replace(".mkv", ".mp4")
                    downloaded_files.append(filepath)
            except Exception as e:
                await msg.edit(f"Download error: {e}")
                continue

        if not downloaded_files:
            return await msg.edit("Failed to download any videos.")

        for file in downloaded_files:
            await app.send_video(
                chat_id=chat_id,
                video=file,
                reply_to_message_id=message.id
            )
            os.remove(file)

        await msg.delete()

    except Exception as e:
        await msg.delete()
        return await message.reply(f"Something went wrong: {e}")