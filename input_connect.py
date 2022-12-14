import statistics
from dataset import DataSet


def append_dict(dictionary: dict, key, value):
    """Добавить значение в лист по ключу"""
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)


def get_key_to_mean(dictionary: dict):
    """Возвращает словарь, значениями которого являются среднее значения входного словаря

    Returns:
        dict: Словарь ключ к среднему листа
    """
    return {key: 0 if not values_list else int(statistics.mean(values_list)) for key, values_list in dictionary.items()}


def get_key_to_count(dictionary: dict):
    """Возвращает словарь, значениями которого являются длина значения входного словаря

    Returns:
        dict: Словарь ключ к длине листа
    """
    return {key: len(values_list) for key, values_list in dictionary.items()}


def sort_by_key(dictionary: dict):
    """Возвращает словарь, отсортированный по ключам"""
    return dict(sorted(dictionary.items()))


def take_top_10(dictionary: dict):
    """Возвращает словарь с 10 лучшими значениями входного словаря"""
    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True)[:10])


class InputConnect:
    """Класс для вводы данных и всей обработки.
    Attributes:
        file_name (str): Название файла
        job_name (str): Название профессии
        year_to_salary (dict): Словарь от года к средней зарплате
        year_to_vacancies_count (dict): Словарь от года к количеству ваканский
        job_year_to_salary (dict): Словарь от года к средней зарплате профессии
        job_year_to_vacancies_count (dict): Словарь от года к количеству вакансий профессии
        city_to_salary (dict): Словарь от города к средней зарплате
        city_to_vacancies_share (dict): Словарь от города к доле от общего числа вакансий
    """
    def __init__(self):
        """Инициаализирует объект InputConnect, обрабатывает файл с вакансиями"""
        self.file_name = input("Введите название файла: ")
        self.job_name = input("Введите название профессии: ")
        self.year_to_salary = {}
        self.year_to_vacancies_count = {}
        self.job_year_to_salary = {}
        self.job_year_to_vacancies_count = {}
        self.city_to_salary = {}
        self.city_to_vacancies_share = {}
        self.__process_data(DataSet(self.file_name).vacancies)

    def print_vacancies(self):
        """Печатает всю статистику по вакансиям"""
        print(f'Динамика уровня зарплат по годам: {self.year_to_salary}')
        print(f'Динамика количества вакансий по годам: {self.year_to_vacancies_count}')
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {self.job_year_to_salary}')
        print(f'Динамика количества вакансий по годам для выбранной профессии: {self.job_year_to_vacancies_count}')
        print(f'Уровень зарплат по городам (в порядке убывания): {self.city_to_salary}')
        print(f'Доля вакансий по городам (в порядке убывания): {self.city_to_vacancies_share}')

    def __process_data(self, vacancies):
        """Обрабатывает данные по вакансиям и задаёт атрибутам класса нужныые значения

        Args:
            vacancies (list): Список вакансий
        """
        if not vacancies:
            return
        years_statistics = {}
        job_statistics = {}
        cities_statistics = {}
        for vacancy in vacancies:
            name = vacancy.name
            salary = vacancy.salary
            city = vacancy.city
            year = vacancy.year
            append_dict(years_statistics, year, salary)
            if self.job_name in name:
                append_dict(job_statistics, year, salary)
            append_dict(cities_statistics, city, salary)
        if len(job_statistics) == 0:
            for year in years_statistics:
                job_statistics[year] = []
        self.__change_years_stats(years_statistics)
        self.__change_job_stats(job_statistics)
        self.__change_cities_stats(cities_statistics)

    def __change_years_stats(self, years_statistics: dict):
        """Сортирует и задает общей статистике нужные значения"""
        self.year_to_salary = sort_by_key(get_key_to_mean(years_statistics))
        self.year_to_vacancies_count = sort_by_key(get_key_to_count(years_statistics))

    def __change_job_stats(self, job_statistics: dict):
        """Сортирует и задает статистике профессии нужные значения"""
        self.job_year_to_salary = sort_by_key(get_key_to_mean(job_statistics))
        self.job_year_to_vacancies_count = sort_by_key(get_key_to_count(job_statistics))

    def __change_cities_stats(self, cities_statistics: dict):
        """Сортирует и задает статистике городов нужные значения"""
        vacancies_count = sum(len(salaries_list) for salaries_list in cities_statistics.values())
        city_to_vacancies_share = get_key_to_count(cities_statistics)
        city_to_vacancies_share = {city: count / vacancies_count for city, count in city_to_vacancies_share.items()}
        city_to_vacancies_share = {k: round(v, 4) for k, v in city_to_vacancies_share.items() if v >= 0.01}
        good_cities = city_to_vacancies_share.keys()
        city_to_salary = get_key_to_mean(cities_statistics)
        city_to_salary = {city: salary for city, salary in city_to_salary.items() if city in good_cities}
        self.city_to_salary = take_top_10(city_to_salary)
        self.city_to_vacancies_share = take_top_10(city_to_vacancies_share)
