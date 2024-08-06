from aiogram.utils.i18n import gettext as _

from utils.db.models import Vacancy


def get_vacancy_menu_message_by_(vacancy: Vacancy) -> str:
    """Returns formatted vacancy menu message by the given vacancy."""
    city = vacancy.city
    if vacancy.remote:
        city = _("віддалена робота")
    elif vacancy.relocate:
        city = _("за кордоном")
    return _(
        "<b>Меню пошуку</b>\n\n{active}\n\n"
        "Категорія: {category}\nДосвід: {exp}\nМісто: {city}\n\n"
        "Пошуковий запит: {search} {descr}\n"
    ).format(
        active=(
            _("Шукаєте роботу зараз")
            if vacancy.active
            else _("Не шукаєте роботу зараз")
        ),
        category=vacancy.category,
        exp=_("Без досвіду") if not vacancy.exp else vacancy.exp,
        city=city,
        search="-" if not vacancy.search else vacancy.search,
        descr=_("(шукати в описах вакансій)") if vacancy.descr else "",
    )
