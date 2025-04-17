from pyrogram import Client, filters
from pyrogram.types import Message
import os
import ffmpeg
import asyncio

# Ensure the 'downloads' folder exists
os.makedirs("downloads", exist_ok=True)

@app.on_message(filters.command("rename") & filters.reply)
async def rename_file(client, message: Message):
    # Check if the file is a supported type (document, video, or audio)
    if not message.reply_to_message.document and not message.reply_to_message.video:
        return await message.reply("Reply to a document, audio, or video to rename it.")

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        return await message.reply("Usage: /rename new_filename.ext", quote=True)

    new_name = args[1]
    file_msg = message.reply_to_message
    downloading = await message.reply("Downloading file...")

    # Download the file to a local path
    file_path = await file_msg.download()

    # Set up the new path with the new filename
    new_path = f"downloads/{new_name}"

    # Rename the file (just changing the name, size and format changes later if needed)
    os.rename(file_path, new_path)

    # If it's a video file, convert and resize it
    if file_msg.video:
        new_name_resized = f"downloads/Resized_{new_name}"
        await resize_video(new_path, new_name_resized)

        # Now, we’ll send the resized video as a Telegram-friendly video
        await downloading.edit("Uploading resized and renamed video...")
        await message.reply_video(video=new_name_resized, caption=f"Renamed and resized to {new_name}")

        # Clean up after upload
        os.remove(new_name_resized)
    else:
        # If it's a document, just send back the renamed document
        await downloading.edit("Uploading renamed file...")
        await message.reply_document(document=new_path, caption=f"Renamed to {new_name}")

    # Clean up the original downloaded file
    os.remove(new_path)
    await downloading.delete()


# Function to resize the video to 1GB by adjusting bitrate and making it larger
async def resize_video(input_path, output_path):
    # Get video duration (important for determining the bitrate)
    probe = ffmpeg.probe(input_path, v='error', select_streams='v:0', show_entries='stream=duration')
    duration = float(probe['streams'][0]['duration'])

    # Set the target size (in bytes) and calculate the target bitrate
    target_size = 1 * 1024 * 1024 * 1024  # 1 GB in bytes
    target_bitrate = (target_size * 8) / duration  # Bitrate = size / duration in bits

    # Convert bitrate to kilobits per second
    target_bitrate_kbps = target_bitrate / 1000

    try:
        # Resize and encode the video to the target bitrate (1GB) using compatible codecs
        ffmpeg.input(input_path).output(output_path, video_bitrate=str(int(target_bitrate_kbps)) + 'k', 
                                        vcodec="libx264", acodec="aac", strict="-2", threads=4).run()

        # Ensure the output video is compatible with Telegram
        ffmpeg.input(output_path).output(output_path, vcodec="libx264", acodec="aac", format="mp4").run()
    except Exception as e:
        print(f"Error while resizing video: {e}")