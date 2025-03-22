import os
import asyncio
from re import findall
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from AnonXMusic import app

DOWNLOAD_DIR = "downloads"

YTDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'merge_output_format': 'mp4',
    'outtmpl': f'{DOWNLOAD_DIR}/%(title).70s.%(ext)s',
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
}


@app.on_message(filters.command(["vid", "video"], prefixes=["/", "!"]))
async def video_search(client: Client, message: Message):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Give me something to search! Example: `/vid cats lim=1`")

    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "")
    except IndexError:
        lim = 1  # Default 1 video

    status = await message.reply("Searching for videos...")

    search_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
    }

    try:
        with YoutubeDL(search_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{lim}:{query}", download=False)
            entries = info.get("entries", [])
            if not entries:
                return await status.edit("No videos found.")
    except Exception as e:
        return await status.edit(f"Search failed: {e}")

    downloaded = []

    for i, entry in enumerate(entries):
        try:
            url = f"https://www.youtube.com/watch?v={entry['id']}"
            await status.edit(f"Downloading video {i+1}: {entry['title'][:50]}")

            with YoutubeDL(YTDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                # Auto-fix extensions
                if not file_path.endswith(".mp4"):
                    base = os.path.splitext(file_path)[0]
                    file_path = base + ".mp4"
                if os.path.exists(file_path):
                    downloaded.append(file_path)
        except Exception as e:
            print(f"Error downloading: {e}")
            continue

    if not downloaded:
        return await status.edit("Failed to download any videos.")

    await status.edit("Uploading to Telegram...")

    for video in downloaded:
        try:
            # Check if under 50MB (Telegram bot limit)
            if os.path.getsize(video) > 50 * 1024 * 1024:
                await message.reply(f"❌ Skipping `{os.path.basename(video)}` — too large.")
                os.remove(video)
                continue

            await client.send_video(
                chat_id=message.chat.id,
                video=video,
                caption=f"Here's your video!",
                reply_to_message_id=message.id
            )
            os.remove(video)
        except Exception as e:
            await message.reply(f"Failed to upload video: {e}")
            if os.path.exists(video):
                os.remove(video)

    await status.delete()