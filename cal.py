import calendar
from django.utils import timezone


class Day:
    """ Day Class """

    def __init__(self, number, is_past):
        self.number = number
        self.is_past = is_past

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    """ Calendar Class """

    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.month_names = (
            "January",
            "Feburary",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        now = timezone.now()
        today = now.day
        month = now.month
        for week in weeks:
            for day, _ in week:
                is_past = False
                if self.month <= month:
                    is_past = bool(day < today or self.month < month)
                new_day = Day(day, is_past)
                days.append(new_day)
        return days

    def get_month(self):
        return self.month_names[self.month - 1]
