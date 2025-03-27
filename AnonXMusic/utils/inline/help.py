from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AnonXMusic import app


def help_pannel(_, page: int = 1, START: Union[bool, int] = None):
    close_button = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    back_button = [InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")]

    mark = back_button if START else close_button

    if page == 1:
        buttons = [
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
                navigation_buttons = [
        InlineKeyboardButton(text="๏ ᴍᴇɴᴜ ๏", callback_data="back_to_main"),
        InlineKeyboardButton(text="๏ ɴᴇxᴛ ๏", callback_data="help_next_2")
    ]
    buttons.append(navigation_buttons)
    return InlineKeyboardMarkup(buttons)
    else:
        buttons = [
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
            ],
            [
                InlineKeyboardButton(text=" Back", callback_data="help_page_1"),
            ],
            close_button,
        ]

    return InlineKeyboardMarkup(buttons)


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")]]
    )


def private_help_panel(_):
    return [
        [InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help")]
    ]