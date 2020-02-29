import calendar


class Calendar:
    """ Calendar Class """

    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.day_names = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
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

    def get_month(self):
        return self.month_names[self.month - 1]
