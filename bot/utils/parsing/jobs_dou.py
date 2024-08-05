from collections import OrderedDict

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def parse_dou_vacancies_from_(url: str):
    """Parses vacancies from DOU by the given params and language code."""
    response = requests.get(url, headers={"user-agent": generate_user_agent()})

    if response.ok:
        return _parse_(response.text)
    raise ValueError("Response is not OK")


def _parse_(html: str):
    """Parses vacancies from HTML."""
    soup = BeautifulSoup(html, "lxml")

    vacancies = OrderedDict()

    for vacancy in soup.find_all("li", class_="l-vacancy"):
        vacancy_link = vacancy.find("a", class_="vt")
        company_link = vacancy.find("a", class_="company")

        vacancies[vacancy_link.get("href")] = {
            "date": vacancy.find("div", class_="date").text.strip(),
            "title": vacancy_link.text.strip(),
            "company": {
                "title": company_link.text.strip(),
                "link": company_link.get("href"),
            },
            "city": vacancy.find("span", class_="cities").text.strip(),
            "description": vacancy.find("div", class_="sh-info").text.strip(),
        }
    return vacancies
