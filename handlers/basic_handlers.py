from aiogram import types
from aiogram.dispatcher import FSMContext
from config import bot_logger
from create_bot import bot, dp
from states.states_group import FSMState
from keyboards.basic_keyboards import cancel_keyboard
from parser.bestchange_parser import ExchangeAnalyst
from parser.parser_exceptions import ExchangeNotFoundException
from requests.exceptions import ConnectionError


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message) -> None:
    """
    Команда старт. Предлагает ввести id обменника на Bestchange для анализа.

    :param message: объект сообщения
    :type message: types.Message
    :return: None
    """

    tg_id = message.from_user.id
    await FSMState.analise_exchange.set()
    await bot.send_message(tg_id, 'Добрый день! Пожалуйста, введите id обменника на bestchange.ru для анализа.\n'
                                  'Для отмены операции введите "отмена".',
                           reply_markup=await cancel_keyboard())


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message) -> None:
    """
    Команда help. Рассказывает о том, что делает бот.

    :param message: объект сообщения
    :type message: types.Message
    :return: None
    """

    tg_id = message.from_user.id
    await bot.send_message(tg_id, 'Добрый день! Я помогу вам проанализировать курс любого обменника с bestchange.ru '
                                  'для пары BTC/USDT и сравню его с лучшим доступным курсом.\n'
                                  'Для того, чтобы начать введите <b>/start</b>',
                           parse_mode='HTML')


@dp.message_handler(lambda msg: msg.text.isdigit(), state=FSMState.analise_exchange)
async def analise_exchange_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер, проводящий анализ обменника

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    tg_id = message.from_user.id
    exchange_id = message.text
    try:
        exchange_analyst = ExchangeAnalyst(exchange_id)
        diff_with_best = await exchange_analyst.get_diff_with_best()

        await state.finish()
        await bot.send_message(tg_id, f'Разница выбранного обменника с лучшим курсом для BTS/USDT: {diff_with_best}')
        await bot.send_message(tg_id, 'Чтобы проанализировать другой обменник, повторно введите <b>/start</b>.',
                               parse_mode='HTML')
    except ExchangeNotFoundException:
        await bot.send_message(tg_id, f'Не удалось найти обменник с id {exchange_id}\n'
                                      f'Попробуйте ещё раз или введите "Отмена".',
                               reply_markup=await cancel_keyboard())
    except ConnectionError:
        await state.finish()
        await bot.send_message(tg_id, 'Не удалось подключиться к bestchange.ru.\n'
                                      'Повторите попытку позже. Для этого введите <b>/start</b>.',
                               parse_mode='HTML')
    except Exception as exc:
        await state.finish()
        await bot.send_message(tg_id, 'Произошла непредвиденная ошибка.\n'
                                      'Повторите попытку позже. Для этого введите <b>/start</b>\n'
                                      'В случае повторения ошибки, напишите разработчику: @alex_solokhin',
                               parse_mode='HTML')
        bot_logger.error(f'Произошла ошибка при работе бота. Пользователь: {tg_id}. Ошибка: {exc}')


@dp.message_handler(lambda msg: msg.text.lower() == 'отмена', state=FSMState.analise_exchange)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер обрабатывает кейс, когда пользователь ввёл "Отмена"

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    tg_id = message.from_user.id
    await state.finish()
    await bot.send_message(tg_id, f'Анализ обменника отменён.')
    await bot.send_message(tg_id, 'Для начала нового анализа введите <b>/start</b>.',
                           reply_markup=await cancel_keyboard(),
                           parse_mode='HTML')


@dp.message_handler(state=FSMState.analise_exchange)
async def try_again_handler(message: types.Message) -> None:
    """
    Хэндлер обрабатывает кейс, в котором пользователь ввёл что-то помимо ID или "Отмена"

    :param message: объект сообщения
    :type message: types.Message
    :return: None
    """

    tg_id = message.from_user.id
    await bot.send_message(tg_id, 'ID обменника может содержать только цифры. Попробуйте ещё раз или введите "Отмена".')
