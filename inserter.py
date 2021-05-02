import connection
import pandas as pd
import os

filename = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'Employee_monthly_salary.csv')
file_open = pd.read_csv('datasets\\Employee_monthly_salary',sep=',',encoding='UTF-8')
print(file_open.head())
