from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewLine3(StatesGroup):
    view_list_line3_state = State()
    user_view_state = State()
    verification_user = State()


class ViewSquad(StatesGroup):
    user_view_state = State()
