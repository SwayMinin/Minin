import csv
from vacancy import Vacancy


class DataSet:
    """Класс для обработки и хранения данных вакансий

    Attributes:
        file_name (str): Название файла с данными
        vacancies (list): Список вакансий
    """
    def __init__(self, file_name):
        """Инициализирует объект DataSet, читает вакансии

        Args:
            file_name (str): Название файла с данными
        """
        self.file_name = file_name
        self.vacancies = list(self.__read_csv(file_name))

    @staticmethod
    def __read_csv(file_name):
        """Лениво возвращает список с данными вакансий, а в случае ошибки - пустой список

        Args:
            file_name (str): Название файла
        """
        with open(file_name, encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            try:
                headers = next(reader)
            except StopIteration:
                print("Пустой файл")
                return []
            filtered = filter(lambda x: len(x) == len(headers) and '' not in x, reader)
            try:
                yield Vacancy(dict(zip(headers, next(filtered))))
            except StopIteration:
                print("Нет данных")
                return []
            for row in filtered:
                yield Vacancy(dict(zip(headers, row)))
