import os
import shutil
from re import findall
from bing_image_downloader import downloader
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, Message
from AnonXMusic import app

@app.on_message(filters.command(["img", "image"], prefixes=["/", "!", "."]))
async def google_img_search(client: Client, message: Message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Provide an image query to search!")

    # Parse lim= value
    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "").strip()
    except IndexError:
        lim = 7

    download_dir = "downloads"

    try:
        # Start downloading images
        await message.reply("Scraping images, please wait...")
        downloader.download(query, limit=lim, output_dir=download_dir, adult_filter_off=True, force_replace=True, timeout=60)
        
        images_dir = str(os.path.join(download_dir, query))  # Explicitly convert Path to string

        # Ensure the directory exists (check using os.path.isdir)
        if not os.path.isdir(images_dir):
            raise Exception(f"Directory {images_dir} does not exist or no images were downloaded.")

        # List images and check if they are valid images
        lst = [os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.endswith((".jpg", ".png"))][:lim]
        
        if not lst:
            raise Exception("No images were downloaded.")
    except Exception as e:
        return await message.reply(f"Error during download: {e}")

    try:
        # Send media group to the chat
        await app.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=img) for img in lst],
            reply_to_message_id=message.id
        )
    except Exception as e:
        return await message.reply(f"Error sending images: {e}")
    finally:
        # Clean up the downloaded images folder after usage
        shutil.rmtree(images_dir, ignore_errors=True)