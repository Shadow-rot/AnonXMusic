from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory
import asyncio
import random

from AnonXMusic import userbot as us, app
from AnonXMusic.core.userbot import assistants

@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    # Check if it's a reply or if username/ID is provided
    if not message.reply_to_message and len(message.text.split()) < 2:
        return await message.reply("Please provide a username/ID or reply to a user's message using /sg!")

    # Get user ID from reply or argument
    if message.reply_to_message:
        args = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1]

    lol = await message.reply("waittttt...")

    try:
        user = await client.get_users(f"{args}")
    except Exception:
        return await lol.edit("<code>Please provide a valid username or ID!</code>")

    # Choose a random Sangmata bot
    sg_bot = random.choice(["sangmata_bot", "sangmata_beta_bot"])

    # Select available userbot assistant
    if 1 in assistants:
        ubot = us.one
    else:
        return await lol.edit("No assistant userbot is available.")

    try:
        a = await ubot.send_message(sg_bot, str(user.id))
        await a.delete()
    except Exception as e:
        return await lol.edit(f"<code>{e}</code>")

    await asyncio.sleep(1)

    async for stalk in ubot.search_messages(a.chat.id):
        if stalk.text:
            await message.reply(stalk.text)
            break
    else:
        await message.reply("The bot didn't return any data.")

    # Delete chat history with Sangmata bot
    try:
        user_info = await ubot.resolve_peer(sg_bot)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass

    await lol.delete()