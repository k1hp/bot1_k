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
        print(need_names)
        if need_names is None:
            print("Новых групп не обнаружено")
            return None
        need_groups = filter(lambda el: el[0] in need_names, self.groups)
        faculties = dict(self._get_facs())
        print(faculties)
        groups_data = []
        for name, url, parameters in need_groups:
            course = parameters[-1][-2::].replace("=", "")
            faculty = parameters[0][-2::].replace("=", "")
            result = {"course": int(course), "faculty": faculties[faculty], "name": name, "url": url}
            groups_data.append(result)
        self.insert_big_data(Group, groups_data)


if __name__ == '__main__':
    psd = GroupsUpdater()
# print(psd.names)