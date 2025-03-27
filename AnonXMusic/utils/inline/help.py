from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic import app

def help_pannel(_, PAGE: int = 1):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]

    if PAGE == 1:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
                    InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
                    InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4"),
                    InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5"),
                    InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7"),
                    InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8"),
                    InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10"),
                    InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11"),
                    InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13"),
                    InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14"),
                    InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15"),
                ],
                [
                    InlineKeyboardButton(text="➡ Next", callback_data="help_next"),
                ],
                first,
            ]
        )
    else:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16"),
                    InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17"),
                    InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_19"], callback_data="help_callback hb19"),
                    InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20"),
                    InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22"),
                    InlineKeyboardButton(text=_["H_B_23"], callback_data="help_callback hb23"),
                    InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_25"], callback_data="help_callback hb25"),
                    InlineKeyboardButton(text=_["H_B_26"], callback_data="help_callback hb26"),
                    InlineKeyboardButton(text=_["H_B_27"], callback_data="help_callback hb27"),
                ],
                [
                    InlineKeyboardButton(text=_["H_B_28"], callback_data="help_callback hb28"),
                    InlineKeyboardButton(text=_["H_B_29"], callback_data="help_callback hb29"),
                    InlineKeyboardButton(text=_["H_B_30"], callback_data="help_callback hb30"),
                ],
                [
                    InlineKeyboardButton(text="⬅ Back", callback_data="help_back"),
                    InlineKeyboardButton(text="🏠 Main Menu", callback_data="help_main"),
                ],
                first,
            ]
        )

    return upl


@app.on_callback_query()
async def help_callback(client, callback_query):
    data = callback_query.data

    # Fetch translations (if needed)
    _ = {
        "CLOSE_BUTTON": "❌ Close",
        "BACK_BUTTON": "⬅ Back",
        "H_B_1": "Help 1", "H_B_2": "Help 2", "H_B_3": "Help 3",
        "H_B_4": "Help 4", "H_B_5": "Help 5", "H_B_6": "Help 6",
        "H_B_7": "Help 7", "H_B_8": "Help 8", "H_B_9": "Help 9",
        "H_B_10": "Help 10", "H_B_11": "Help 11", "H_B_12": "Help 12",
        "H_B_13": "Help 13", "H_B_14": "Help 14", "H_B_15": "Help 15",
        "H_B_16": "Help 16", "H_B_17": "Help 17", "H_B_18": "Help 18",
        "H_B_19": "Help 19", "H_B_20": "Help 20", "H_B_21": "Help 21",
        "H_B_22": "Help 22", "H_B_23": "Help 23", "H_B_24": "Help 24",
        "H_B_25": "Help 25", "H_B_26": "Help 26", "H_B_27": "Help 27",
        "H_B_28": "Help 28", "H_B_29": "Help 29", "H_B_30": "Help 30",
    }

    if data == "help_next":
        await callback_query.message.edit_reply_markup(help_pannel(_, PAGE=2))
    elif data == "help_back":
        await callback_query.message.edit_reply_markup(help_pannel(_, PAGE=1))
    elif data == "help_main":
        await callback_query.message.edit_reply_markup(help_pannel(_, PAGE=1))  # Set to main panel
    else:
        pass  # Handle other buttons if needed