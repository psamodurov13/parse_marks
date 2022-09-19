from oauth2client.service_account import ServiceAccountCredentials
import time
import gspread as gs
import datetime
import requests as rq
import os
from bs4 import BeautifulSoup as bs

# Указываем путь к JSON с ключомhe
CREDENTIALS_FILE = '/home/parse_marks/credentials.json'
# CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")


# Функция добавления строки с показателями в Google Sheet
def add_to_gsheet(result):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    gc = gs.authorize(credentials)
    # Проверяем начался ли новый месяц
    wks = gc.open('Sheets-1').worksheet(result[1][3:])
    wks.append_row(result)


# Словарь со списком проверяемых товаров {'id': 'url}
products = {'61333': 'https://vkusvill.ru/goods/pitstsa-chiken-pesto-okhlazhdennaya-61333.html',
            '45516': 'https://vkusvill.ru/goods/pitstsa-gavayskaya-okhlazhdennaya-45516.html',
            '45520': 'https://vkusvill.ru/goods/pitstsa-4-syra-okhlazhdennaya-45520.html',
            '66710': 'https://vkusvill.ru/goods/pitstsa-margarita-350-g-66710.html'}
result_e = ['Вечер', datetime.date.today().strftime('%d.%m.%Y')]
for product in products:
    response_marks = rq.get(
        f'https://vkusvill.ru/ajax/product_comments/from_api/comments_load.php?id={product}')
    soup = bs(response_marks.text, 'html.parser')
    marks_ev = [i.text for i in soup.find_all('span', class_='ProductCommentsRating--cnt')]
    result_e.extend(marks_ev)
    result_e.append('')
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
gc = gs.authorize(credentials)
result_m = gc.open('Sheets-1').worksheet(result_e[1][3:]).row_values(gc.open('Sheets-1').worksheet(result_e[1][3:]).find(result_e[1]).row)
print(result_e)
print(result_m)
add_to_gsheet(result_e)
print('Готово вечер')
# Считаем разницу между вечерними и утренними данными
result_diff = [datetime.date.today().strftime('%d.%m.%Y')]
result_diff.insert(0, 'Разница')
for i in range(2, 26):
    if '.' not in result_m[i] and result_e[i].isdigit():
        result_diff.append(int(result_e[i]) - int(result_m[i]))
    else:
        result_diff.append('')
print('diff - ', result_diff)
add_to_gsheet(result_diff)
print('Готово разница')

