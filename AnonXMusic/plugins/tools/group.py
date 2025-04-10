import asyncio
import datetime
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_ID = 17944283          # Replace with your values
API_HASH = "03f2f561ca86def71fe88d3ae16ed529"
BOT_TOKEN = "7945225070:AAEk4zHWvsawtTmCwUkzk_uulPu9gZEjCxg"
OWNER_ID = 5147822244       # Replace with your Telegram user ID

app = Client("vc_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
vc_start_times = {}

@app.on_message(filters.video_chat_started)
async def on_vc_started(_, message: Message):
    vc_start_times[message.chat.id] = datetime.datetime.now()
    await message.reply("Voice chat started.")

@app.on_message(filters.video_chat_ended)
async def on_vc_ended(_, message: Message):
    start = vc_start_times.pop(message.chat.id, None)
    if start:
        duration = datetime.datetime.now() - start
        total_seconds = int(duration.total_seconds())
        h, rem = divmod(total_seconds, 3600)
        m, s = divmod(rem, 60)
        await message.reply(f"Voice chat ended.\nDuration: {h}h {m}m {s}s")
    else:
        await message.reply("Voice chat ended.\nDuration unknown.")

@app.on_message(filters.video_chat_members_invited)
async def on_invited(_, message: Message):
    inviter = message.from_user.mention
    for user in message.video_chat_members_invited.users:
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Mute", callback_data=f"mute_{user.id}"),
                 InlineKeyboardButton("Unmute", callback_data=f"unmute_{user.id}")]
            ])
            await message.reply(
                f"{user.mention} (ID: `{user.id}`) was invited by {inviter}",
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Error: {e}")

@app.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = int(data.split("_")[1])
    action = "Muted" if data.startswith("mute") else "Unmuted"
    try:
        await app.restrict_chat_member(chat_id, user_id, can_send_messages=(action == "Unmuted"))
        await query.answer(action)
    except:
        await query.answer("Failed. Missing permissions?")

@app.on_message(filters.command("math"))
def math_command(_, message: Message):
    if len(message.command) < 2:
        return message.reply("Usage: /math <expression>")
    expr = message.text.split(" ", 1)[1]
    try:
        result = eval(expr)
        message.reply(f"Result: {result}")
    except:
        message.reply("Invalid expression.")

@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def leave(_, message: Message):
    await message.reply("Leaving group...")
    await app.leave_chat(message.chat.id)

async def main():
    await app.start()
    print("Bot is running.")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())