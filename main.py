from input_connect import InputConnect
from report import Report


if __name__ == "__main__":
    inp_connect = InputConnect()
    Report.generate_pdf(inp_connect)
