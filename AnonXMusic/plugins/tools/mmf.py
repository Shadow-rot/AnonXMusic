import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from pyrogram import filters
from pyrogram.types import Message
from AnonXMusic import app

@app.on_message(filters.command("mmf"))
async def mmf(_, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message

    if not reply_message or not reply_message.media:
        return await message.reply_text("Reply to an image/video/gif with `/mmf your text`", quote=True)

    if len(message.text.split()) < 2:
        return await message.reply_text("**Give me text after /mmf to memify.**")

    msg = await message.reply_text("Processing...")

    text = message.text.split(None, 1)[1]
    media = await app.download_media(reply_message)

    if media.endswith((".jpg", ".jpeg", ".png", ".webp")):
        meme = await drawText(media, text)
        await app.send_document(chat_id, document=meme)
        os.remove(meme)

    elif media.endswith(".gif") or media.endswith(".mp4") or media.endswith(".mkv"):
        out_path = await add_text_to_video(media, text)
        await app.send_video(chat_id, video=out_path)
        os.remove(out_path)

    else:
        await message.reply_text("Unsupported media type.")
    
    await msg.delete()
    if os.path.exists(media):
        os.remove(media)

# PIL image meme
async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./AnonXMusic/assets/default.ttf"

    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text, lower_text = text, ""

    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5

    # Draw upper text
    for u_text in textwrap.wrap(upper_text, width=15):
        width, height = draw.textsize(u_text, font=m_font)
        x = (i_width - width) / 2
        y = int((current_h / 640) * i_width)
        draw.text((x, y), u_text, font=m_font, fill="white")
        current_h += height + pad

    # Draw lower text
    for l_text in textwrap.wrap(lower_text, width=15):
        width, height = draw.textsize(l_text, font=m_font)
        x = (i_width - width) / 2
        y = i_height - height - int((20 / 640) * i_width)
        draw.text((x, y), l_text, font=m_font, fill="white")

    output = "memify.webp"
    img.save(output, "webp")
    return output

# Video or gif meme using MoviePy
async def add_text_to_video(file_path, text):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    w, h = clip.size

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text, lower_text = text, ""

    # TextClip config
    txt_clips = []
    if upper_text:
        txt1 = TextClip(upper_text, fontsize=50, color='white', font='Arial-Bold', method='caption', size=(w, None)).set_position(('center', 'top')).set_duration(duration)
        txt_clips.append(txt1)

    if lower_text:
        txt2 = TextClip(lower_text, fontsize=50, color='white', font='Arial-Bold', method='caption', size=(w, None)).set_position(('center', 'bottom')).set_duration(duration)
        txt_clips.append(txt2)

    video = CompositeVideoClip([clip, *txt_clips])
    output_path = "memify_video.mp4"
    video.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4, logger=None)
    return output_path