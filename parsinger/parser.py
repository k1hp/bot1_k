import requests
from typing import List, Tuple
from bs4 import BeautifulSoup
import lxml
from datetime import datetime

from others.settings import BASE_URL, GROUPS_URL
from helpers.times import Clocks
from time import perf_counter


class Parser:
    def __init__(self):
        ...

    # config = Preparations()  # добавить прокси и тп

    def _do_request(self, url: str) -> requests.Response:
        return requests.get(url)

    def _do_requests(self, urls: List[str]) -> List[requests.Response]:
        start_time = perf_counter()
        with requests.Session() as session:
            session.headers.update({'User-Agent': 'Mozilla/5.0'})
            results = []
            for url in urls:
                response = session.get(url)
                results.append(response)
            print(f"Итоговое время: {perf_counter()-start_time}")
            return results


    def _create_soup(self, html_text: str) -> BeautifulSoup:
        return BeautifulSoup(html_text, 'lxml')

    def _get_soups(self, urls: List[str]) -> List[BeautifulSoup]:
        results = self._do_requests(urls)
        return [self._create_soup(res.text) for res in results]


class GroupsParser(Parser):
    def __init__(self):
        self.__base_response: requests.Response = self._do_request(BASE_URL)
        self.__soup = self._create_soup(self.__base_response.text)
        self.__clocks = Clocks()

    def __get_parameters(self, parameter: str) -> List[tuple]:
        result = self.__soup.select_one(f"select[name={parameter}]").select("option")
        lst = [(el.attrs["value"], el.string) for el in result]
        return lst[1:]

    def _get_pers(self) -> List[tuple]:
        return self.__get_parameters("pers")

    def _get_facs(self) -> List[tuple]:  # value, fac
        return self.__get_parameters("facs")

    def _get_courses(self):  # value, cor
        return self.__get_parameters("courses")

    def __create_facs_urls(self) -> List[str]:
        pers = self._get_pers()
        period = self.__clocks.define_need_period(map(lambda x: x[-1], pers), datetime.today())
        filtered_period = filter(lambda el: el[-1] == period.__str__(), pers).__next__()
        facs = self._get_facs()
        courses = self._get_courses()
        urls = list()
        for fac in facs:
            for course in courses:
                urls.append(GROUPS_URL + f"&pers={filtered_period[0]}&facs={fac[0]}&courses={course[0]}")
        return urls

    def get_groups(self) -> List[Tuple]:  # name, url
        urls = self.__create_facs_urls()
        soups = self._get_soups(urls)
        groups = list()
        for soup in soups:
            try:
                result = soup.select_one(".table-responsive a.btn")
                groups.append((result.string, result.attrs["href"]))
            except Exception as e:
                print("Нет групп", e)
        return groups

    def links_generation(self):
        self.get_groups()


class Timetable:  # превращает ссылку в расписание
    ...

if __name__ == '__main__':
    parser = GroupsParser()
    print(parser.get_groups())
