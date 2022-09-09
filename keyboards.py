from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



inline_kb_full = InlineKeyboardMarkup(row_width=3).add()
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))

def make_inline_keybord(ids):
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    for i in ids:
        inline_kb_full.add(InlineKeyboardButton(i, callback_data=i))
    return inline_kb_full
