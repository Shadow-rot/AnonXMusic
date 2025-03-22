import os
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from AnonXMusic import app  # use your own app/client if different

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

YTDL_OPTS = {
    "format": "mp4",
    "outtmpl": f"{DOWNLOAD_DIR}/%(title).70s.%(ext)s",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "merge_output_format": "mp4"
}


@app.on_message(filters.command(["vid", "video"], prefixes=["/", "!"]))
async def youtube_video(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("**Please provide a search query.**\n\nExample: `/vid cat video`")

    query = message.text.split(None, 1)[1]
    await message.reply_chat_action("typing")

    search_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "default_search": "ytsearch1"
    }

    try:
        with YoutubeDL(search_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if not search_result or not search_result.get("entries"):
                return await message.reply("No results found.")

            video_data = search_result["entries"][0]
            video_url = f"https://www.youtube.com/watch?v={video_data['id']}"
            video_title = video_data.get("title", "video")

        status = await message.reply(f"**Downloading:** `{video_title}`")

        with YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4"):
                filename = os.path.splitext(filename)[0] + ".mp4"

        # Check size
        file_size = os.path.getsize(filename)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            os.remove(filename)
            return await status.edit("❌ The downloaded video is too large to send via bot (limit: 50MB).")

        await client.send_video(
            chat_id=message.chat.id,
            video=filename,
            caption=f"🎬 **{video_title}**",
            reply_to_message_id=message.id
        )

        os.remove(filename)
        await status.delete()

    except Exception as e:
        await message.reply(f"❌ Error: `{str(e)}`")