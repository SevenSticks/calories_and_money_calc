import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, object):
        """Record objects of Record class to the list."""
        self.records.append(object)

    def get_stats(self, days):
        """Can return the amount for any number of days"""
        day_now = dt.date.today()
        delta = day_now - dt.timedelta(days)
        return sum(record.amount for record in self.records
                   if delta <= record.date <= day_now)

    def get_today_stats(self):
        """Sum up amount for today."""
        return self.get_stats(0)

    def get_week_stats(self):
        """Return the count of weekly stats."""
        return self.get_stats(6)

    def get_balance(self):
        return self.limit - self.get_today_stats()


class Record:
    """Сreate an object with the attributes we need,
    check the date and change its format.
    """
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            # Changing date format from dd.mm.yyyy to yyyy-mm-dd
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class CashCalculator(Calculator):
    USD_RATE = 60.20
    EURO_RATE = 80.34

    def get_today_cash_remained(self, currency):
        """Dictionary
        is used to calculate amounts based on currency rates
        and contains currency names.
        """
        balance = self.get_balance()
        if balance == 0:
            return "Денег нет, держись"

        currencies = {"eur": (self.EURO_RATE, "Euro"),
                      "usd": (self.USD_RATE, "USD"),
                      "rub": (1, "руб")}

        if currency not in currencies:
            return f"Нет такой валюты - {currency}!"

        currency_rate, currency_name = currencies[currency]
        currency_rest = balance / currency_rate

        if currency_rest > 0:
            return (f"На сегодня осталось "
                    f"{currency_rest:.2f} {currency_name}")

        currency_rest = abs(currency_rest)
        return (f"Денег нет, держись: твой долг - "
                f"{currency_rest:.2f} {currency_name}")


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """This method counts the remaining calories."""

        balance = self.get_balance()

        if balance > 0:
            return ("Сегодня можно съесть что-нибудь ещё,"
                    f" но с общей калорийностью не более {balance} кКал")
        return "Хватит есть!"


if __name__ == "__main__":
    # CASH #
    r1 = Record(amount=100, comment="Безудержный шопинг")
    r2 = Record(amount=100, comment="Наполнение потребительской корзины",
                date="21.08.2020")
    r3 = Record(amount=100, comment="Катание на такси", date="30.08.2020")

    cash_calc = CashCalculator(1000)
    cash_calc.add_record(r1)
    cash_calc.add_record(r2)
    cash_calc.add_record(r3)

    print(cash_calc.get_today_cash_remained("rub"))
    print(cash_calc.get_week_stats())

    # CALORIES #
    r4 = Record(amount=100,
                comment="Кусок тортика. И ещё один.",
                date="20.08.2020")

    r5 = Record(amount=100,
                comment="Йогурт.")

    r6 = Record(amount=100,
                comment="Баночка чипсов.",
                date="24.02.2019")

    calories_calc = CaloriesCalculator(1000)
    calories_calc.add_record(r4)
    calories_calc.add_record(r5)
    calories_calc.add_record(r6)

    print(calories_calc.get_calories_remained())
    print(calories_calc.get_week_stats())
