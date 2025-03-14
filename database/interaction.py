from database.creation import Session, Base, Group, engine
from datetime import date
from typing import List, Tuple, Optional
from sqlalchemy import insert
import json

from helpers.managers import TimetableManager
from helpers.times import Clocks
from others.settings import BASE_URL
from parsinger.parser import GroupsParser


class DataBase:
    def insert_big_data(self, table: Base, data: List[dict]) -> None:
        with Session() as session:
            session.execute(insert(table), data)
            session.commit()

    def get_data(self, table: Base) -> List[Base]:
        with Session() as session:
            return session.query(table).all()

    def create_all(self):
        Base.metadata.create_all(engine)

    def drop_table(self, table: Base) -> None:
        Base.metadata.drop_all(engine, tables=[table.__table__])


class GroupsUpdater(DataBase, GroupsParser):
    def __init__(self):
        super().__init__()
        self.groups = self.get_groups()
        self.names = list(map(lambda x: x[0], self.groups))
        # for name, url, parameters in self.groups:
        #     self.names.append(name)
        self.update_groups()

    def check_groups(self) -> Optional[Tuple[str]]:
        existing_names = [el.name for el in self.get_data(Group)]
        intersect_names = set(self.names).difference(existing_names)
        if intersect_names != set():
            return tuple(intersect_names)

    def update_groups(self) -> None:
        need_names = self.check_groups()
        if need_names is None:
            print("Новых групп не обнаружено")
            return None
        need_groups = filter(lambda el: el[0] in need_names, self.groups)
        faculties = dict(self._get_value_facs())
        groups_data = []
        for name, url, parameters in need_groups:
            course = parameters[-1][-2::].replace("=", "")
            faculty = parameters[0][-2::].replace("=", "")
            result = {"course": int(course), "faculty": faculties[faculty], "name": name, "url": url}
            groups_data.append(result)
        self.insert_big_data(Group, groups_data)

class TimetableAdder(DataBase):
    def __init__(self, parser: GroupsParser, table: Base) -> None:
        self.parser = parser
        self.table = table
        clocks = Clocks()
        parameters = clocks.get_latest_params(parser.pers)
        self.parameters = (self.__convert_dict_str(parameters[0]), self.__convert_dict_str(parameters[1]))

    @staticmethod
    def __convert_dict_str(data: dict) -> str:
        return "".join([f'&{key}={value}' for key, value in data.items()])

    def __links_generation(self):
        links = []
        for row in self.get_data(self.table):
            links.append(BASE_URL+ row.url + self.parameters[0])
            links.append(BASE_URL + row.url + self.parameters[1])
        return links

    def get_timetables(self):
        row_name = "group_name" if self.table == Group else "teacher_name"
        links = self.__links_generation()
        print(f"Начало сбора данных {links.__len__()}")

        # soups = self.parser.get_soups(links[:2])
        soups = self.parser.get_soups(links)
        print("Конец сбора данных")
        timetables = [TimetableManager(soup, row_name).data for soup in soups]
        print(timetables)


    def add_timetables(self):
        self.drop_table(self.table)
        self.create_all()

if __name__ == '__main__':
    # psd = GroupsUpdater()
    fd = TimetableAdder(GroupsParser(), Group)
    print(fd.get_timetables())