import datetime
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

# Assuming you have a config.py file with your API values and OWNER_ID
from config import OWNER_ID, API_ID, API_HASH, BOT_TOKEN

# Initialize bot
app = Client("vcbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to track VC start times
vc_start_times = {}

# Voice chat started
@app.on_message(filters.video_chat_started)
async def on_vc_start(_, msg: Message):
    vc_start_times[msg.chat.id] = datetime.datetime.now()
    await msg.reply("Voice chat started.")

# Voice chat ended
@app.on_message(filters.video_chat_ended)
async def on_vc_end(_, msg: Message):
    start_time = vc_start_times.pop(msg.chat.id, None)
    if start_time:
        duration = datetime.datetime.now() - start_time
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await msg.reply(f"Voice chat ended.\nDuration: {hours}h {minutes}m {seconds}s")
    else:
        await msg.reply("Voice chat ended.\nDuration: Unknown")

# When users are invited to the voice chat
@app.on_message(filters.video_chat_members_invited)
async def on_user_invited(client: Client, message: Message):
    inviter = message.from_user.mention
    invited_users = message.video_chat_members_invited.users

    for user in invited_users:
        try:
            mention = user.mention
            user_id = user.id
            text = (
                f"{mention} (ID: `{user_id}`) joined the voice chat.\n"
                f"Invited by: {inviter}"
            )
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Mute", callback_data=f"mute_{user_id}"),
                    InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")
                ]
            ])
            await message.reply(text, reply_markup=keyboard)
        except Exception as e:
            print(f"Error: {e}")

# Handle mute/unmute button actions
@app.on_callback_query()
async def handle_callback(client: Client, callback: CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id

    if data.startswith("mute_") or data.startswith("unmute_"):
        user_id = int(data.split("_")[1])
        try:
            if data.startswith("mute_"):
                await client.restrict_chat_member(chat_id, user_id, can_send_messages=False)
                await callback.answer("Muted")
            else:
                await client.restrict_chat_member(chat_id, user_id, can_send_messages=True)
                await callback.answer("Unmuted")
        except Exception as e:
            await callback.answer("Failed: Bot might not have sufficient rights.")

# Math command
@app.on_message(filters.command("math"))
def calculate_math(_, message: Message):
    if len(message.command) < 2:
        return message.reply("Usage: /math <expression>")
    expression = message.text.split(" ", 1)[1]
    try:
        result = eval(expression)
        message.reply(f"The result is: {result}")
    except:
        message.reply("Invalid expression")

# Leave group command (owner only)
@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def leave_group(_, message: Message):
    await message.reply("Successfully leaving the group.")
    await app.leave_chat(message.chat.id, delete=True)

# Run the bot
app.run()