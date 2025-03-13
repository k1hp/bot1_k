from database.creation import Session, Base, Group
from datetime import date
from typing import List, Tuple, Optional
from sqlalchemy import insert
import json

from parsinger.parser import GroupsParser


class DataBase:
    def insert_big_data(self, table: Base, data: List[dict]) -> None:
        with Session() as session:
            session.execute(insert(table), data)
            session.commit()

    def get_data(self, table: Base) -> List[Base]:
        with Session() as session:
            return session.query(table).all()


class UpdatingGroups(DataBase, GroupsParser):
    def __init__(self):
        super().__init__()
        self.names = []
        self.groups = self.get_groups()
        for name, url in self.groups:
            self.names.append(name)
        self.update_groups()

    def check_groups(self) -> Optional[Tuple[str]]:
        existing_names = [el.name for el in self.get_data(Group)]
        intersect_names = set(self.names).difference(existing_names)
        if intersect_names != set():
            return tuple(intersect_names)

    def update_groups(self) -> None:
        need_names = self.check_groups()
        print(need_names)
        if need_names is None:
            print("Новых групп не обнаружено")
            return None
        name_url_lst = filter(lambda el: el[0] in need_names, self.groups)
        print(self._get_facs())
        faculties = dict(self._get_facs())
        groups_data = []
        for name, url in name_url_lst:
            parameters = url.split("&")[-2::]
            print(parameters)
            result = {"course": parameters[0][-1], "faculty": faculties[parameters[-1][-1]], "name": name, "url": url}
            groups_data.append(result)
        print(groups_data)



psd = UpdatingGroups()