import imghdr
import os
from asyncio import gather
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AnonXMusic import app
from config import BOT_USERNAME
from AnonXMusic.utils.errors import capture_err
from AnonXMusic.utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)
from AnonXMusic.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

MAX_STICKERS = 120
SUPPORTED_TYPES = ["jpeg", "png", "webp"]

# /get_sticker command
@app.on_message(filters.command("get_sticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r or not r.sticker:
        return await message.reply("Reply to a sticker.")

    m = await message.reply("Sending...")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        message.reply_photo(f),
        message.reply_document(f),
    )

    await m.delete()
    os.remove(f)

# /kang command
@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ/ɪᴍᴀɢᴇ/ᴀɴɪᴍᴀᴛɪᴏɴ ᴛᴏ ᴋᴀɴɢ ɪᴛ...")
    if not message.from_user:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴ ᴀᴅᴍɪɴ, ᴋᴀɴɢ sᴛɪᴄᴋᴇʀs ɪɴ ᴍʏ ᴘᴍ.....")

    msg = await message.reply_text("ᴋᴀɴɢɪɴɢ.....")

    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🤔"

    is_animated = False
    is_video = False
    doc = message.reply_to_message.photo or message.reply_to_message.document

    try:
        if message.reply_to_message.sticker:
            is_animated = message.reply_to_message.sticker.is_animated
            is_video = message.reply_to_message.sticker.is_video
            sticker = await create_sticker(
                await get_document_from_file_id(message.reply_to_message.sticker.file_id),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10_000_000:
                return await msg.edit("ғɪʟᴇ sɪᴢᴇ ɪs ᴛᴏᴏ ʟᴀʀɢᴇ.")

            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)

            if image_type not in SUPPORTED_TYPES:
                return await msg.edit(f"ғᴏʀᴍᴀᴛ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ! ({image_type})")

            try:
                temp_file_path = await resize_file_to_sticker_size(temp_file_path)
            except OSError as e:
                await msg.edit("Failed to resize image.")
                raise Exception(f"Resize error at {temp_file_path}; {e}")

            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )

            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("ᴄᴀɴ'ᴛ ᴋᴀɴɢ ᴛʜɪs ᴍᴇssᴀɢᴇ....")

    except Exception as e:
        await message.reply_text(str(e))
        print(format_exc())
        return

    packnum = 0
    limit = 0

    while True:
        if is_animated:
            if packnum == 0:
                packname = f"a{message.from_user.id}_by_{botname_clean}"
            else:
                packname = f"a{packnum}_{message.from_user.id}_by_{botname_clean}"
        elif is_video:
            if packnum == 0:
                packname = f"v{message.from_user.id}_by_{botname_clean}"
            else:
                packname = f"v{packnum}_{message.from_user.id}_by_{botname_clean}"
        else:
            if packnum == 0:
                packname = f"f{message.from_user.id}_by_{botname_clean}"
            else:
                packname = f"f{packnum}_{message.from_user.id}_by_{botname_clean}"

        try:
            stickerset = await get_sticker_set_by_name(client, packname)

            if not stickerset:
                title_prefix = "animated" if is_animated else "video" if is_video else "kang"
                await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s {title_prefix} pack",
                    packname,
                    [sticker],
                )
                break

            elif len(stickerset.stickers) >= MAX_STICKERS:
                packnum += 1
                limit += 1
                if limit >= 50:
                    return await msg.edit("ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ.")
                continue

            else:
                await add_sticker_to_set(client, stickerset, sticker)
                break

        except (PeerIdInvalid, UserIsBlocked):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Start", url=f"https://t.me/{botname_clean}")]
            ])
            return await msg.edit(
                "Start a private chat with me first...",
                reply_markup=keyboard,
            )
        except StickerEmojiInvalid:
            return await msg.edit("Invalid emoji.")
        except Exception as e:
            print(format_exc())
            return await msg.edit(f"Error: {e}")

    await msg.edit(
        f"sᴛɪᴄᴋᴇʀ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ #{packnum + 1}!\nᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴ",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("View Pack", url=f"https://t.me/addstickers/{packname}")]
        ])
    )