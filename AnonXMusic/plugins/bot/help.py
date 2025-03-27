from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from AnonXMusic import app
from AnonXMusic.utils.database import get_lang
from AnonXMusic.utils.decorators.language import LanguageStart, languageCB
from AnonXMusic.utils.inline.help import ( 
    help_back_markup,
    private_help_panel,
    first_page,
    second_page  # Ensure second_page is imported
)
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = private_help_panel(_)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = private_help_panel(_)
        await update.reply_video(
            video=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    # Navigation between help pages
    if cb == "next":
        await CallbackQuery.edit_message_text(
            "🔹 **Help - Page 2** 🔹", reply_markup=second_page(_)
        )
        return
    elif cb == "back":
        await CallbackQuery.edit_message_text(
            "🔹 **Help - Page 1** 🔹", reply_markup=private_help_panel(_)
        )
        return

    keyboard = help_back_markup(_)

    help_dict = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
        "hb16": helpers.HELP_16,
        "hb17": helpers.HELP_17,
        "hb18": helpers.HELP_18,
        "hb19": helpers.HELP_19,
        "hb20": helpers.HELP_20,
        "hb21": helpers.HELP_21,
        "hb22": helpers.HELP_22,
        "hb23": helpers.HELP_23,
        "hb24": helpers.HELP_24,
        "hb25": helpers.HELP_25,
        "hb26": helpers.HELP_26,
        "hb27": helpers.HELP_27,
        "hb28": helpers.HELP_28,
        "hb29": helpers.HELP_29,
        "hb30": helpers.HELP_30,
    }

    if cb in help_dict:
        await CallbackQuery.edit_message_text(help_dict[cb], reply_markup=keyboard)