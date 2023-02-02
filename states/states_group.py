from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMState(StatesGroup):
    analise_exchange = State()
