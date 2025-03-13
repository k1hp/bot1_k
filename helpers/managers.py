import requests
from bs4 import BeautifulSoup
from copy import copy
from typing import Optional
import json


class TimetableManager:
    def __init__(self, soup, row_name):
        self.__key_names = ("lesson", "time", "discipline", "teacher", "location")
        self.__soup = soup
        self.__template_dict = {row_name: self.__get_name()}
        self.__data = self.__fill_data()

    @property
    def data(self):
        return self.__data

    def __get_name(self) -> str:
        return self.__soup.select_one("h1").string.split(" ")[2]

    def __fill_data(self):
        result = []
        for tag in self.__soup.select("table.table-bordered"):
            print(tag)
            buffer = copy(self.__template_dict)
            buffer["date"] = self.__get_date(tag)
            buffer["body"] = self.__get_json(tag)
            if buffer["date"] is not None and buffer["body"] != []:
                result.append(buffer)
        return result

    @staticmethod
    def __get_date(tag) -> Optional[str]:
        try:
            return tag.select_one("th").string
        except:
            print("Нет занятий")
            return None

    def __get_json(self, tag) -> str:
        trs = tag.select("tr")
        lst = []
        for cell in trs:
            result = {}
            print(lst)
            for td, key in zip(cell.select("td"), self.__key_names):
                print(td.string)
                if key != "discipline":
                    if td.string is None:
                        try:
                            result[key] = lst[-1][key]
                        except IndexError or KeyError:
                            break
                    elif td.string == "Занятий нет":
                        break
                    else:
                        result[key] = td.string
                else:
                    if td.b is None:
                        break
                    result[key] = "***".join((td.b.string, td.string if td.string else "", td.small.string))
            else:
                if result:
                    lst.append(result)
        json_string = json.dumps(lst)
        return json.loads(json_string)


# response = requests.get(
#     "https://mauniver.ru/student/timetable/new/schedule.php?key=2eca0871-18e8-11ef-9f67-1cc1de6f817c&perstart=2025-03-10&perend=2025-03-16&perkind=%D0%BD")
# soup = BeautifulSoup(response.text, "html.parser")
# u = TimetableManager(soup, "group_name")
# print(u.data)
