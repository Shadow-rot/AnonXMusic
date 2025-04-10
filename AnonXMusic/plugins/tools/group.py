import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from AnonXMusic import app
from config import OWNER_ID

# Dictionary to store VC start times per chat
vc_start_times = {}

@app.on_message(filters.video_chat_started)
async def vc_started(_, msg):
    chat_id = msg.chat.id
    vc_start_times[chat_id] = datetime.datetime.now()
    await msg.reply("Voice chat started.")

@app.on_message(filters.video_chat_ended)
async def vc_ended(_, msg):
    chat_id = msg.chat.id
    start_time = vc_start_times.pop(chat_id, None)
    if start_time:
        duration = datetime.datetime.now() - start_time
        seconds = duration.total_seconds()
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours}h {minutes}m {seconds}s"
        await msg.reply(f"Voice chat ended\nDuration: {time_str}")
    else:
        await msg.reply("Voice chat ended\nDuration: Unknown")

@app.on_message(filters.video_chat_members_invited)
async def on_user_invited(app: Client, message: Message):
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
                [InlineKeyboardButton("Mute", callback_data=f"mute_{user_id}"),
                 InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")]
            ])

            await message.reply(text, reply_markup=keyboard)
        except Exception:
            pass

@app.on_callback_query()
async def handle_vc_controls(client, callback_query: CallbackQuery):
    data = callback_query.data
    if data.startswith("mute_") or data.startswith("unmute_"):
        user_id = int(data.split("_")[1])
        chat_id = callback_query.message.chat.id

        try:
            if data.startswith("mute_"):
                await client.restrict_chat_member(chat_id, user_id, can_send_messages=False)
                await callback_query.answer("Muted")
            else:
                await client.restrict_chat_member(chat_id, user_id, can_send_messages=True)
                await callback_query.answer("Unmuted")
        except Exception:
            await callback_query.answer("Failed. Bot may need admin rights.")

@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):   
    expression = message.text.split("/math ", 1)[1]
    try:        
        result = eval(expression)
        response = f"The result is: {result}"
    except:
        response = "Invalid expression"
    message.reply(response)

@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    await message.reply_text("Successfully left.")
    await app.leave_chat(chat_id=chat_id, delete=True)