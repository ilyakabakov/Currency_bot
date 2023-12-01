from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from database.parser import CurrencyParser
from initialize import dp, bot
from keyboards import start_page_kb

currency_parser = CurrencyParser()

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            text="Показать курс валют к Рублю?\n"
                "Или конвертировать цену?",
            reply_markup=start_page_kb)
    except Exception as ex:
        print(f'ERROR: {ex}')

async def edit_message_with_currency(callback: types.CallbackQuery, base_currency, target_currency):
    value = await currency_parser.get_data(query='Valute', currency=target_currency)
    result = round(1 / value, 4)
    float_result = float(result)
    await currency_parser.update_data()
    await callback.message.edit_text(
        text=f"Текущий курс:\n"
             f"1 {base_currency} = {float_result} {target_currency}\n"
             f"1 {target_currency} = {value} {base_currency}",
        reply_markup=start_page_kb
    )

@dp.callback_query_handler(Text(startswith='/gel'))
async def currency_gel(callback: types.CallbackQuery):
    await edit_message_with_currency(callback, 'RUB', 'GEL')



@dp.callback_query_handler(Text(startswith='/usd'))
async def currency_gel(callback: types.CallbackQuery):
    await edit_message_with_currency(callback, 'RUB', 'USD')

class FSMGel(StatesGroup):
    price = State()

@dp.callback_query_handler(Text(startswith='/price_gel_to_rub'))
async def start_fsm_price(callback: types.CallbackQuery):
    await FSMGel.price.set()
    await callback.message.edit_text('Введи цену:')


@dp.message_handler(state=FSMGel.price)
async def load_price_gel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    value = await currency_parser.get_data(query='Valute', currency='GEL')
    result = float(data['price']) * value
    await state.finish()
    await message.answer(
        text=f"Цена продукта:\n\n"
             f"{data['price']} GEL = {round(result, 2)} RUB",

    )
    await message.answer("Показать курс валют к Рублю?\n"
                        "Или конвертировать цену?",
                         reply_markup=start_page_kb)


