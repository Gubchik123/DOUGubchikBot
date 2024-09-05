import logging
from collections import OrderedDict

import requests
import cloudscraper
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from data.config import COOKIES, HEADERS


def parse_dou_vacancies_from_(url: str):
    """Parses vacancies from DOU by the given params and language code."""
    HEADERS["user-agent"] = generate_user_agent()
    response = requests.get(url, headers=HEADERS, cookies=COOKIES)

    if response.ok:
        return _parse_(response.text)
    if response.status_code == 403:
        tokens, user_agent = cloudscraper.get_tokens(
            "https://jobs.dou.ua/vacancies/"
        )
        logging.info(f"Tokens: {tokens=}, {user_agent=}")
    raise ValueError(f"Response is not OK: {response.status_code}")


def _parse_(html: str):
    """Parses vacancies from HTML."""
    soup = BeautifulSoup(html, "lxml")

    vacancies = OrderedDict()

    for vacancy in soup.find_all("li", class_="l-vacancy"):
        vacancy_link = vacancy.find("a", class_="vt")
        company_link = vacancy.find("a", class_="company")
        city = vacancy.find("span", class_="cities")
        salary = vacancy.find("span", class_="salary")

        vacancies[vacancy_link.get("href")] = {
            "date": vacancy.find("div", class_="date").text.strip(),
            "title": vacancy_link.text.strip(),
            "company": {
                "title": company_link.text.strip(),
                "link": company_link.get("href"),
            },
            "city": city.text.strip() if city else "",
            "salary": salary.text.strip() if salary else "",
            "description": vacancy.find("div", class_="sh-info").text.strip(),
        }
    return vacancies
