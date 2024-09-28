from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from config import bot, dp, staff
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BotBlocked


class FSM_Order(StatesGroup):
    article = State()
    size = State()
    quantity = State()
    contacts = State()
    confirm = State()

async def start_order(message: types.Message):
    await message.answer('Введите артикул товара: ', reply_markup=buttons.cancel_button)
    await FSM_Order.article.set()

async def ordered_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text

    await message.answer('Введите размер товара: ')
    await FSM_Order.next()

async def ordered_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Выберите количество товара: ')
    await FSM_Order.next()

async def ordered_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await message.answer('Введите ваши контакты: ')
    await FSM_Order.next()

async def ordered_contacts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contacts'] = message.text

    await message.answer('Верные ли данные ?')
    await message.answer(
                f'Артикул: {data["article"]}\n'
                f'Размер товара: {data["size"]}\n'
                f'Количество товара: {data["quantity"]}\n'
                f'Ваши контакты: {data["contacts"]}\n',
        reply_markup=buttons.submit_button)

    await FSM_Order.confirm.set()

async def confirm_order(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        data = await state.get_data()
        order_info = (f"Новый заказ:\n"
                      f"Артикул: {data['article']}\n"
                      f"Размер товара: {data['size']}\n"
                      f"Количество товара: {data['quantity']}\n"
                      f"Ваши контакты: {data['contacts']}")

        for staff_id in staff:
            try:
                await bot.send_message(staff_id, order_info)
                await message.answer(f'Заказ успешно отправлен сотруднику с ID: {staff_id}')
            except BotBlocked:
                await message.answer(f'Не удалось отправить заказ сотруднику с ID: {staff_id}, '
                                     f'так как бот был заблокирован этим пользователем. ')
            except Exception as e:
                await message.answer(f'Не удалось отправить новый заказ сотруднику с ID: {staff_id}. Ошибка {e}')

        await state.finish()
        await message.answer("Ваш заказ успешно отправлен!", reply_markup=ReplyKeyboardRemove())
    elif message.text.lower() == 'нет':
        await state.finish()
        await message.answer("Ваш заказ отменен.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите 'Да' или 'Нет'.")



def register_order_handler(dp: Dispatcher):
    dp.register_message_handler(start_order, commands=['order'])
    dp.register_message_handler(ordered_article, state=FSM_Order.article)
    dp.register_message_handler(ordered_size, state=FSM_Order.size)
    dp.register_message_handler(ordered_quantity, state=FSM_Order.quantity)
    dp.register_message_handler(ordered_contacts, state=FSM_Order.contacts)
    dp.register_message_handler(confirm_order, state=FSM_Order.confirm)