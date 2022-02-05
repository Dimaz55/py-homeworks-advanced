from datetime import datetime
from application.db.people import get_employees
from application.salary import calculate_salary

if __name__ == '__main__':
    print('Текущая дата:', datetime.date(datetime.today()))
    calculate_salary()
    get_employees()


