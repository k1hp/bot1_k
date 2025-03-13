from database.creation import Session, Group, GroupTimetable
from datetime import date

session = Session()
group1 = Group(course=1, faculty="ИПАТ", name="вася", url="fnd")
group2 = Group(course=2, faculty="ИВТ", name="ВП", url="fnd1")

timetable1 = GroupTimetable(group=group1, date=date(day=1, month=1, year=2021), body=None)
timetable2 = GroupTimetable(group=group2, date=date(day=1, month=2, year=2021), body=None)



if __name__ == "__main__":
    session = Session()
    session.add_all([timetable1, timetable2])
    session.commit()
    # проверить гибридный is_empty
    select = session.query(GroupTimetable).all()
    for row in select:
        print(row.is_empty)