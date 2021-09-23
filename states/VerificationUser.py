from aiogram.dispatcher.filters.state import StatesGroup, State


class VerificationUser(StatesGroup):
    user_call_state = State()
    user_pay_state = State()
    user_send_pay_data_state = State()
    finish_state = State()

