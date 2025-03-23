import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from yt_dlp import YoutubeDL
from AnonXMusic import app  # Use your Client/app

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

YTDL_OPTS = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
    "outtmpl": f"{DOWNLOAD_DIR}/%(title).70s.%(ext)s",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "merge_output_format": "mp4",
    "cookies": "cookies.txt",  # <== Confirm this file path is correct!
}


@app.on_message(filters.command(["vid", "video"], prefixes=["/", "!"]))
async def youtube_video(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("**Please provide a search query.**\n\nExample: `/vid cat videos`")

    query = message.text.split(None, 1)[1]
    await message.reply_chat_action(ChatAction.TYPING)

    search_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "default_search": "ytsearch1",
        "cookiefile": "cookies.txt"
    }

    try:
        with YoutubeDL(search_opts) as ydl:
            result = ydl.extract_info(f"ytsearch1:{query}", download=False)
            entries = result.get("entries")
            if not entries:
                return await message.reply("No videos found.")

            video = entries[0]
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            video_title = video.get("title", "video")

        status = await message.reply(f"**Downloading:** `{video_title}`")

        with YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4"):
                filename = os.path.splitext(filename)[0] + ".mp4"

        size = os.path.getsize(filename)
        if size > 50 * 1024 * 1024:
            os.remove(filename)
            return await status.edit("❌ Video is larger than 50MB. Can't send.")

        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)

        await client.send_video(
            chat_id=message.chat.id,
            video=filename,
            caption=f"🎬 **{video_title}**",
            reply_to_message_id=message.id
        )

        os.remove(filename)
        await status.delete()

    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")