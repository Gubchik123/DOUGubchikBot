from typing import Dict, List, Union

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..models import Vacancy
from ..db import LocalSession, add_commit_and_refresh


vacancies_cache: Dict[int, Vacancy] = {}


def create_vacancy_for_(user_chat_id: int, state_data: dict) -> Vacancy:
    """Creates a new vacancy for user with the given user chat id."""
    return add_commit_and_refresh(
        Vacancy(
            id_user_id=user_chat_id,
            active=state_data.get("active", True),
            url_prefix=state_data.get("url_prefix", "vacancies"),
            last_job_urls=state_data.get("last_job_urls"),
            category=state_data.get("category"),
            exp=state_data.get("exp"),
            city=state_data.get("city"),
            remote=state_data.get("remote", False),
            relocate=state_data.get("relocate", False),
            descr=state_data.get("descr", False),
            search=state_data.get("search"),
        )
    )


def _get_vacancy_by_(
    session: Session, user_chat_id: int
) -> Union[Vacancy, None]:
    """Returns a vacancy by the given user chat id."""
    return (
        session.query(Vacancy)
        .filter(Vacancy.id_user_id == user_chat_id)
        .first()
    )


def get_vacancy_by_(user_chat_id: int) -> Union[Vacancy, None]:
    """Returns a vacancy by the given user chat id."""
    if user_chat_id in vacancies_cache:
        return vacancies_cache[user_chat_id]

    with LocalSession() as session:
        vacancy = _get_vacancy_by_(session, user_chat_id)
        if vacancy is not None:
            vacancies_cache[user_chat_id] = vacancy
    return vacancy


def get_all_active_vacancies() -> List[Vacancy]:
    """Returns all active vacancies."""
    with LocalSession() as session:
        return session.query(Vacancy).filter(Vacancy.active).all()


def update_vacancy_with_(user_chat_id: int, **fields):
    """Updates a vacancy by the given user chat id with the given fields."""
    with LocalSession() as session:
        session.execute(
            update(Vacancy)
            .where(Vacancy.id_user_id == user_chat_id)
            .values(**fields)
        )
        session.commit()

    if user_chat_id in vacancies_cache:
        for field, value in fields.items():
            setattr(vacancies_cache[user_chat_id], field, value)
