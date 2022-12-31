from input_connect import InputConnect
from report import Report


if __name__ == "__main__":
    output_data = input('dasdadasdasdВведите данные для печати: ')
    inp_connect = InputConnect()
    if output_data == 'Вакансии':
        inp_connect.print_vacancies()
    if output_data == 'Статистика':
        Report.generate_pdf(inp_connect)
