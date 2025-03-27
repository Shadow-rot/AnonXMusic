from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Function for the help panel with pagination
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

# Function for back button
def help_back_markup():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="⬅ Back", callback_data="help_back")]]
    )

# Function for private help panel
def private_help_panel():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="🔙 Back", callback_data="help_back")]]
    )