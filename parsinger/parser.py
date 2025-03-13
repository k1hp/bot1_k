import requests
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup
import lxml
from datetime import datetime

from others.settings import BASE_URL, GROUPS_URL
from helpers.times import Clocks
from time import perf_counter
from others.decorators import filter_tuples


class Parser:
    def __init__(self):
        ...

    # config = Preparations()  # добавить прокси и тп

    def do_request(self, url: str, parameters: Optional[dict] = None) -> requests.Response:
        return requests.get(url, params=parameters)

    def _do_requests(self, urls: List[str]) -> List[requests.Response]:
        start_time = perf_counter()
        print("Начало requests")

        total = len(urls)
        with requests.Session() as session:
            session.headers.update({'User-Agent': 'Mozilla/5.0'})
            results = []
            for index, url in enumerate(urls):
                print(f"\r{index}/{total}", end="")
                response = session.get(url)
                results.append(response)
            print(f"Итоговое время: {perf_counter() - start_time}")
            return results

    def _create_soup(self, html_text: str) -> BeautifulSoup:
        return BeautifulSoup(html_text, 'lxml')

    def get_soups(self, urls: List[str]) -> List[BeautifulSoup]:
        results = self._do_requests(urls)
        return [self._create_soup(res.text) for res in results]


class GroupsParser(Parser):
    def __init__(self):
        self.__base_response: requests.Response = self.do_request(BASE_URL)
        self.__soup = self._create_soup(self.__base_response.text)
        self.__clocks = Clocks()

    def __get_parameters(self, parameter: str) -> List[tuple]:
        result = self.__soup.select_one(f"select[name={parameter}]").select("option")
        lst = [(el.attrs["value"], el.string) for el in result]
        return lst[1:]

    @property
    @filter_tuples
    def pers(self) -> Tuple[str]:
        return self.__get_parameters("pers")

    @property
    @filter_tuples
    def facs(self) -> Tuple[str]:  # value, fac
        return self.__get_parameters("facs")

    @property
    @filter_tuples
    def courses(self) -> Tuple[str]:  # value, cor
        return self.__get_parameters("courses")

    def _get_value_pers(self) -> List[tuple]:
        return self.__get_parameters("pers")

    def _get_value_facs(self) -> List[tuple]:  # value, fac
        return self.__get_parameters("facs")

    def _get_value_courses(self) -> List[tuple]:  # value, cor
        return self.__get_parameters("courses")

    def __create_facs_urls(self) -> List[str]:
        pers = self._get_value_pers()
        period = self.__clocks.define_need_period(map(lambda x: x[-1], pers), datetime.today())
        filtered_period = filter(lambda el: el[-1] == period.__str__(), pers).__next__()
        facs = self._get_value_facs()
        courses = self._get_value_courses()
        urls = list()
        for fac in facs:
            for course in courses:
                urls.append(GROUPS_URL + f"&pers={filtered_period[0]}&facs={fac[0]}&courses={course[0]}")
        return urls

    def get_groups(self) -> List[Tuple]:  # name, url
        urls = self.__create_facs_urls()
        soups = self.get_soups(urls)
        groups = list()
        for soup, url in zip(soups, urls):
            try:
                result = soup.select_one(".table-responsive").select("a.btn")
                parameters = url.split("&")[-2::]
                for element in result:
                    url = element.attrs["href"].split("&")[0]
                    groups.append((element.string, url, parameters))
            except Exception as e:
                print("Нет групп", e)

        return groups

    class TeacherParser(Parser):
        def __init__(self):
            ...


if __name__ == '__main__':
    parser = GroupsParser()
    print(parser.get_groups())
