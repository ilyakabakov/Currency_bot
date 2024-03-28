from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    btns = [
        types.InlineKeyboardButton(text='GEL', callback_data='gel'),
        types.InlineKeyboardButton(text='USD', callback_data='usd'),
        types.InlineKeyboardButton(text='KZT', callback_data='kzt'),
        types.InlineKeyboardButton(text='Цена из GEL в RUB', callback_data='price_gel_to_rub'),
    ]
    kb.add(*btns)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    btn = [
        types.InlineKeyboardButton(text='Cancel', callback_data='cancel')
    ]
    kb.add(*btn)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)