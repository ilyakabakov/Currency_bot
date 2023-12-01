from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_page_kb = InlineKeyboardMarkup(row_width=5)

start_page_btn_1 = InlineKeyboardButton(text='GEL', callback_data='/gel')
start_page_btn_2 = InlineKeyboardButton(text='USD', callback_data='/usd')
start_page_btn_3 = InlineKeyboardButton(text='Цена из GEL в RUB', callback_data='/price_gel_to_rub')

start_page_kb.add(start_page_btn_1,
                  start_page_btn_2).add(start_page_btn_3)