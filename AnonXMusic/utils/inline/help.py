from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic import app

def generate_help_buttons(_, start: int, end: int, page: int):
    return [[InlineKeyboardButton(text=_[f"H_B_{i}"], callback_data=f"help_callback hb{i}_p{page}")] 
            for i in range(start, end + 1)]

def help_panel(_, page: int):
    buttons = generate_help_buttons(_, start=(page - 1) * 15 + 1, end=min(page * 15, 25), page=page)
    
    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="๏ ʙᴀᴄᴋ ๏", callback_data=f"help_page_{page - 1}"))
    navigation.append(InlineKeyboardButton(text="๏ ᴍᴇɴᴜ ๏", callback_data="back_to_main"))
    if page * 15 < 25:
        navigation.append(InlineKeyboardButton(text="๏ ɴᴇxᴛ ๏", callback_data=f"help_page_{page + 1}"))

    buttons.append(navigation)
    return InlineKeyboardMarkup(buttons)

def help_back_markup(_, page):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"help_back_{page}"),
                                  InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]])

def private_help_panel(_):
    return [[InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help")]]