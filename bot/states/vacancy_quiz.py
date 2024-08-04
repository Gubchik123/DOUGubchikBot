from aiogram.fsm.state import State, StatesGroup


class VacancyQuiz(StatesGroup):
    """States to create a vacancy."""

    category = State()
    exp = State()
    city = State()
    is_search = State()
    search = State()
    descr = State()
    active = State()
