from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationUser(StatesGroup):
    user_invite_state = State()
    user_contact_state = State()