from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.parser import CurrencyParser
from initialize import bot
from keyboards import get_menu_keyboard, cancel_kb

currency_parser = CurrencyParser()
router = Router()
@router.message(CommandStart())
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            text="Показать курс валют к Рублю?\n"
                "Или конвертировать цену?",
            reply_markup=get_menu_keyboard())
    except Exception as ex:
        print(f'ERROR: {ex}')

async def edit_message_with_currency(callback: types.CallbackQuery, base_currency, target_currency):
    value = await currency_parser.get_data(query='Valute', currency=target_currency)
    result = round(1 / value, 4)
    message_text = (
        f"Текущий курс:\n"
        f"1 {base_currency} = {result} {target_currency}\n"
        f"1 {target_currency} = {value} {base_currency}"
    )
    await callback.message.edit_text(
        text=message_text,
        reply_markup=get_menu_keyboard()
    )

async def edit_message_with_currency_kzt(callback: types.CallbackQuery, base_currency, target_currency):
    value = await currency_parser.get_data(query='Valute', currency=target_currency)
    base_to_target_rate = round(100 / value, 4)
    target_to_base_rate = round(0.01 * value,4)
    message_text = (
        f"Текущий курс:\n"
        f"1 {base_currency} = {base_to_target_rate} {target_currency}\n"
        f"1 {target_currency} = {target_to_base_rate} {base_currency}"
    )
    await callback.message.edit_text(
        text=message_text,
        reply_markup=get_menu_keyboard()
    )

@router.callback_query(F.data == 'gel')
async def currency_gel(callback: types.CallbackQuery):
    await currency_parser.update_data()
    await edit_message_with_currency(callback, 'RUB', 'GEL')


@router.callback_query(F.data == 'usd')
async def currency_usd(callback: types.CallbackQuery):
    await currency_parser.update_data()
    await edit_message_with_currency(callback, 'RUB', 'USD')

@router.callback_query(F.data =='kzt')
async def currency_usd(callback: types.CallbackQuery):
    await currency_parser.update_data()
    await edit_message_with_currency_kzt(callback, 'RUB', 'KZT')

class FSMGel(StatesGroup):
    price = State()

@router.callback_query(F.data =='price_gel_to_rub')
async def start_fsm_price(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMGel.price)
    await callback.message.edit_text('Введи цену:',
                                     reply_markup=cancel_kb())

@router.callback_query(F.data == 'cancel')
async def cancel_state_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.edit_text(text='Cancelled',
        reply_markup=get_menu_keyboard())
@router.message(FSMGel.price)
async def load_price_gel(message: types.Message, state: FSMContext):

    await state.update_data(price=message.text)
    data = await state.get_data()
    value = await currency_parser.get_data(query='Valute', currency='GEL')
    result = float(data['price']) * value
    await state.clear()
    await message.answer(
        text=f"Цена продукта:\n\n"
             f"{data['price']} GEL = {round(result, 2)} RUB",

    )
    await message.answer("Показать курс валют к Рублю?\n"
                        "Или конвертировать цену?",
                         reply_markup=get_menu_keyboard())


