import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import MONGO_DB_URI

mongo = MongoClient(MONGO_DB_URI)
db = mongo["AnonX"]
warns_db = db["warns"]
limits_db = db["warn_limits"]

# Check if a user is admin
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

@app.on_message(filters.command("warn") & filters.group)
async def warn_user(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can issue warnings.")

    if not message.reply_to_message:
        return await message.reply("Reply to a user to warn them.")

    target_user = message.reply_to_message.from_user

    if await is_admin(client, message.chat.id, target_user.id):
        return await message.reply("You can't warn another admin.")

    user_id = str(target_user.id)
    chat_id = str(message.chat.id)

    user_warn = warns_db.find_one({"chat_id": chat_id, "user_id": user_id})
    current_warns = user_warn["warns"] if user_warn else 0
    current_warns += 1

    warns_db.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"warns": current_warns}},
        upsert=True
    )

    limit_doc = limits_db.find_one({"chat_id": chat_id})
    limit = limit_doc["limit"] if limit_doc else 3

    if current_warns >= limit:
        try:
            await client.kick_chat_member(message.chat.id, target_user.id)
            await message.reply(f"{target_user.mention} has been kicked for reaching {current_warns} warnings.")
            warns_db.delete_one({"chat_id": chat_id, "user_id": user_id})
        except Exception as e:
            await message.reply(f"Failed to kick user: {e}")
    else:
        await message.reply(
            f"{target_user.mention} has been warned.\nTotal Warns: {current_warns}/{limit}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Remove Warn", callback_data=f"removewarn_{chat_id}_{user_id}")]]
            ),
        )

@app.on_callback_query(filters.regex(r"removewarn_(.*)_(.*)"))
async def remove_warn(client, callback_query):
    chat_id, user_id = callback_query.data.split("_")[1:]
    admin_id = callback_query.from_user.id

    if not await is_admin(client, int(chat_id), admin_id):
        return await callback_query.answer("Only admins can remove warnings.", show_alert=True)

    user_warn = warns_db.find_one({"chat_id": chat_id, "user_id": user_id})
    if user_warn and user_warn["warns"] > 0:
        new_warns = user_warn["warns"] - 1
        warns_db.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$set": {"warns": new_warns}},
        )
        await callback_query.answer("Removed one warning.")
        await callback_query.message.edit_text(f"1 warning removed. Total now: {new_warns}")
    else:
        await callback_query.answer("No warnings to remove.", show_alert=True)

@app.on_message(filters.command("warns") & filters.group)
async def check_warns(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    user_id = str(user.id)
    chat_id = str(message.chat.id)
    user_warn = warns_db.find_one({"chat_id": chat_id, "user_id": user_id})
    warns = user_warn["warns"] if user_warn else 0

    limit_doc = limits_db.find_one({"chat_id": chat_id})
    limit = limit_doc["limit"] if limit_doc else 3

    await message.reply(f"{user.mention} has {warns}/{limit} warning(s).")

@app.on_message(filters.command("resetwarns") & filters.group)
async def reset_warns(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can reset warnings.")
    
    if not message.reply_to_message:
        return await message.reply("Reply to a user to reset warnings.")
    
    user_id = str(message.reply_to_message.from_user.id)
    chat_id = str(message.chat.id)
    warns_db.delete_one({"chat_id": chat_id, "user_id": user_id})
    
    await message.reply(f"Warnings for {message.reply_to_message.from_user.mention} have been reset.")

@app.on_message(filters.command("setwarn") & filters.group)
async def set_warn_limit(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can set warn limits.")
    
    if len(message.command) < 2 or not message.command[1].isdigit():
        return await message.reply("Usage: /setwarn <limit_number>")
    
    limit = int(message.command[1])
    chat_id = str(message.chat.id)
    limits_db.update_one({"chat_id": chat_id}, {"$set": {"limit": limit}}, upsert=True)
    await message.reply(f"Warn limit set to {limit} for this group.")