import csv
from vacancy import Vacancy


class DataSet:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.vacancies = list(self.__read_csv(file_name))

    @staticmethod
    def __read_csv(file_name):
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
