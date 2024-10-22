from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def inline_keyboard_smile():
    key_num = ()
    form = InlineKeyboardMarkup(row_width=5)
    key_num += (InlineKeyboardButton('😡', callback_data='1_back'),)
    key_num += (InlineKeyboardButton('🙁', callback_data='2_back'),)
    key_num += (InlineKeyboardButton('😐', callback_data='3_back'),)
    key_num += (InlineKeyboardButton('😏', callback_data='4_back'),)
    key_num += (InlineKeyboardButton('😄', callback_data='5_back'),)
    form.add(*key_num)
    return form