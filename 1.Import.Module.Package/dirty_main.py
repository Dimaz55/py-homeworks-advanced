from datetime import *
from application.db.people import *
from application.salary import *

if __name__ == '__main__':
    print('Текущая дата:', datetime.date(datetime.today()))
    calculate_salary()
    get_employees()