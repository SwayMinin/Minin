currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
}


class Vacancy:
    """Класс для представления вакансии

    Attributes:
        name (str): Название вакансии
        salary (int): Средняя зарплата в рублях
        city (str): Город вакансии
        year (str): Год публикации вакансии
    """
    def __init__(self, row):
        """Инициализирует класс Vacancy, задаёт атрибутам нужные значения

        Args:
            row (dict): Словарь с данными вакансии
        """
        self.name = row['name']
        salary_from = int(float(row['salary_from']))
        salary_to = int(float(row['salary_to']))
        self.salary = (salary_from + salary_to) / 2 * currency_to_rub[row['salary_currency']]
        self.city = row['area_name']
        self.year = int(row['published_at'][:4])
