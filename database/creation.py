from sqlalchemy import create_engine, ForeignKey, JSON, String, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, mapped_column, Mapped
from typing import Optional, List
from others.conf import DB_CONNECTION

Base = declarative_base()
engine = create_engine(DB_CONNECTION)
Session = sessionmaker(bind=engine)

class Timetable:
    @hybrid_property
    def is_empty(self) -> bool:
        if self.date is None or self.body is None:
            return True
        return False


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)

    group: Mapped['Group'] = relationship('Group', back_populates='users')


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    course: Mapped[int] = mapped_column(nullable=False)
    faculty: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship('User', back_populates='group')
    timetables: Mapped[List["GroupTimetable"]] = relationship('GroupTimetable', back_populates='group')


class GroupTimetable(Base, Timetable):
    __tablename__ = 'group_timetable'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    group_name: Mapped[str] = mapped_column(String(50), ForeignKey('groups.name'), nullable=False)
    date: Mapped[str] = mapped_column(String(30), nullable=False)
    body: Mapped[JSON] = mapped_column(JSON)

    group: Mapped['Group'] = relationship('Group', back_populates='timetables')



class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    timetables: Mapped[List["TeacherTimetable"]] = relationship('TeacherTimetable', back_populates='teacher')


class TeacherTimetable(Base, Timetable):
    __tablename__ = 'teacher_timetable'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    teacher_name: Mapped[str] = mapped_column(String(60), ForeignKey('teachers.name'), nullable=False)
    date:  Mapped[str] = mapped_column(String(30), nullable=False)
    body: Mapped[JSON] = mapped_column(JSON)

    teacher: Mapped["Teacher"] = relationship('Teacher', back_populates='timetables')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine, tables=[GroupTimetable.__table__])