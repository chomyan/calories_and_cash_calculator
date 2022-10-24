import datetime as dt

date_format = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = [] #пустой список(массив) для хранения записей

    def add_record(self, next_record: 'Record ') -> None:
        """Добавление новой записи."""
        self.records.append(next_record)

    def get_today_stats(self) -> float:
        """Сколько потрачено за сегодня."""
        d_today = dt.date.today()
        return sum([record.amount
                    for record in self.records
                    if record.date == d_today])

    def get_week_stats(self) -> float:
        """Сколько потрачено за 7 дней."""
        d_today = dt.date.today()
        date_week_ago = d_today - dt.timedelta(days=7)
        return float(sum([record.amount
                         for record in self.records
                         if date_week_ago < record.date <= d_today]))

    def get_today_remained(self) -> float:
        """Сколько еще можно потратить."""
        spent_today = self.get_today_stats()
        return self.limit - spent_today


class CashCalculator(Calculator):
    USD_RATE = 470.0
    EUR_RATE = 480.0
    TG_RATE = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Сколько денег можно еще потратить."""
        all_currency = { 
            'usd':('USD', self.USD_RATE), 
            'eur':('Euro', self.EUR_RATE),
            'tg':('Тенге', self.TG_RATE),
            }

        if currency not in all_currency:
            raise ValueError("Валюта введена некорректно.")
        currency_name, currency_course = all_currency[currency]
        spent_today = self.get_today_remained()
        if spent_today == 0:
            return 'Денег нет, держись'

        today_spent_currency = round(abs(spent_today / currency_course), 2)
        if spent_today > 0:
            return(f'На сегодня осталось {today_spent_currency}'
                   f'{currency_name}')
        else:
            return(f'Денег нет, держись: твой долг - '
                   f'{today_spent_currency} {currency_name}')

class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Сколько можно еще съесть."""
        spent_today = round(self.get_today_remained())
        if spent_today > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {spent_today} кКал')
        else:
            return 'Хватит есть!'

class Record:
    """Создание записи."""
    def __init__(self, amount: float, comment: str, date: str = None):
        self.amount = float(amount)
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()


cash_calculator = CashCalculator(47000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=500, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=4000, comment="Сущи"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=20000, comment="Бар", date="22.10.2022"))
                
print(cash_calculator.get_today_cash_remained("tg")) 

