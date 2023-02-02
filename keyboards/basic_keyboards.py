from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Reply-клавиатура для отмены анализа обменника.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    cancel = KeyboardButton('Отмена')

    keyboard.add(cancel)

    return keyboard
