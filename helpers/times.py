from typing import Optional, List

from others.settings import GROUP_CONFIG_PARAMS

from datetime import datetime, timedelta, date
from typing import List


class Period:
    def __init__(self, gap_string: str):
        self.__format: str = "%d.%m.%Y"
        self.__new_format: str = "%Y-%m-%d"
        self.__gap_string: str = gap_string

        self.__period_list: List[date] = []
        self.__start, self.__end, self.__kind = self.parse_string()
        self.__period_list = self.convert_to_list()

    @property
    def start_string(self) -> str:
        return self.__start.strftime(self.__new_format)

    @property
    def end_string(self) -> str:
        return self.__end.strftime(self.__new_format)

    @property
    def kind(self) -> str:
        return self.__kind

    def check_key(self, key: int) -> int:
        if not isinstance(key, int):
            raise TypeError("Индекс должен быть целым числом")
        if key < -1 or key >= len(self.__period_list):
            raise IndexError("Неверный индекс")
        return key

    def __str__(self):
        return self.__gap_string

    def __len__(self) -> int:
        return len(self.__period_list)

    def __getitem__(self, key: int) -> date:
        key = self.check_key(key)
        return self.__period_list[key]

    def __contains__(self, item: date | datetime) -> bool:
        if isinstance(item, datetime):
            return item.date() in self.__period_list
        return item in self.__period_list

    def __iter__(self):
        yield from self.__period_list

    def parse_string(self) -> tuple:
        parts = self.__gap_string.split()
        if len(parts) != 2:
            raise ValueError("Неверный формат строки. Ожидается 'дата-диапазон тип'.")

        start, end = [
            datetime.strptime(part, self.__format).date()
            for part in parts[0].split("-")
        ]
        kind = parts[1].split("/")[0].strip("(")
        return start, end, kind

    def convert_to_list(self) -> List[date]:

        return [
            self.__start + timedelta(days=i)
            for i in range((self.__end - self.__start).days + 1)
        ]


class Clocks:
    def __init__(self):
        self.today = datetime.today().date()
        self.period_values = {
            "today": self.today,
            "tomorrow": self.today + timedelta(days=1),
            "this_week": self.today,
            "next_week": self.today + timedelta(days=8),
        }

    def get_day_month(self, inp: datetime | date) -> tuple:
        return inp.day, inp.month

    def define_need_period(
        self, periods: List[str], our_date: datetime | date
    ) -> Optional[Period]:
        for element in periods:
            period = Period(element)
            if our_date in period:
                return period

    def get_period_params(self, periods: List[str], our_date: str) -> dict:
        our_date = self.period_values[our_date]
        period: Optional[Period] = self.define_need_period(periods, our_date)
        if period is None:
            raise ValueError("Такого периода не существует")
        data = dict(
            zip(
                GROUP_CONFIG_PARAMS[1:],
                (period.start_string, period.end_string, period.kind),
            )
        )
        return data


if __name__ == "__main__":
    period = "09.09.2024-15.09.2024 (н/н)"
    periods = [
        "02.09.2024-08.09.2024 (ч/н)",
        "09.09.2024-15.09.2024 (н/н)",
        "16.09.2024-22.09.2024 (ч/н)",
        "23.09.2024-29.09.2024 (н/н)",
        "30.09.2024-06.10.2024 (ч/н)",
        "07.10.2024-13.10.2024 (н/н)",
        "14.10.2024-20.10.2024 (ч/н)",
        "21.10.2024-27.10.2024 (н/н)",
        "28.10.2024-03.11.2024 (ч/н)",
        "04.11.2024-10.11.2024 (н/н)",
        "11.11.2024-17.11.2024 (ч/н)",
        "18.11.2024-24.11.2024 (н/н)",
        "25.11.2024-01.12.2024 (ч/н)",
        "02.12.2024-08.12.2024 (н/н)",
        "09.12.2024-15.12.2024 (ч/н)",
        "16.12.2024-22.12.2024 (ч/н)",
        "23.12.2024-29.12.2024 (н/н)",
        "30.12.2024-05.01.2025 (ч/н)",
        "06.01.2025-12.01.2025 (н/н)",
        "13.01.2025-19.01.2025 (ч/н)",
        "20.01.2025-26.01.2025 (н/н)",
        "27.01.2025-02.02.2025 (ч/н)",
        "03.02.2025-09.02.2025 (н/н)",
        "10.02.2025-16.02.2025 (ч/н)",
        "04.03.2025-10.03.2025 (ч/н)",
    ]

    clocks = Clocks()
    cls = Period(period)
    print(cls)
    print(f"Да, нет: {datetime(day=8, month=9, year=2024) in cls}")
    # print(cls.parameters)

    # print(clocks.remake_period(period))
    slc = clocks.define_need_period(
        periods, datetime(day=27, month=1, year=2025)
    ).__str__
    try:
        print(clocks.get_period_params(periods, "tomorrow"))
    except Exception as e:
        print(e)
