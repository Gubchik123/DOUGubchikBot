from utils.parsing.params import Params
from utils.parsing.jobs_dou import parse_dou_vacancies_from_


def update_state_data_with_last_job_urls(state_data: dict):
    """Updates the given state data with parsed last job URLs."""
    params = Params(
        category=state_data.get("category"),
        exp=state_data.get("exp"),
        city=state_data.get("city"),
        remote=state_data.get("remote", False),
        relocate=state_data.get("relocate", False),
        descr=state_data.get("descr", False),
        search=state_data.get("search"),
    )
    vacancies = parse_dou_vacancies_from_(
        url=f"https://jobs.dou.ua/{state_data.get('url_prefix')}/{params}"
    )
    state_data["last_job_urls"] = ",".join(vacancies.keys())
