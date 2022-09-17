from oauth2client.service_account import ServiceAccountCredentials
import time
import gspread as gs
import datetime
import requests as rq
import os
from bs4 import BeautifulSoup as bs

# Указываем путь к JSON с ключом
# CREDENTIALS_FILE = 'credentials.json'
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")


# Функция добавления строки с показателями в Google Sheet
def add_to_gsheet(result):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    gc = gs.authorize(credentials)
    # Проверяем начался ли новый месяц
    if result[1][:2] == '01' and result[0] == 'Утро':
        gc.open('Sheets-1').sheet1.duplicate(new_sheet_name=result[1][3:])
        gc.open('Sheets-1').worksheet(result[1][3:]).delete_rows(start_index=3, end_index=100)
    wks = gc.open('Sheets-1').worksheet(result[1][3:])
    wks.append_row(result)


def main():
    # Словарь со списком проверяемых товаров {'id': 'url}
    products = {'61333': 'https://vkusvill.ru/goods/pitstsa-chiken-pesto-okhlazhdennaya-61333.html',
                '45516': 'https://vkusvill.ru/goods/pitstsa-gavayskaya-okhlazhdennaya-45516.html',
                '45520': 'https://vkusvill.ru/goods/pitstsa-4-syra-okhlazhdennaya-45520.html',
                '66710': 'https://vkusvill.ru/goods/pitstsa-margarita-350-g-66710.html'}
    # 0 - morning, 1 - evening
    counter = 0
    while True:
        if counter == 0:
            result_m = ['Утро', datetime.date.today().strftime('%d.%m.%Y')]
            for product in products:
                response_avg = rq.get(products[product])
                soup_avg = bs(response_avg.text, 'html.parser')
                avg = soup_avg.find('div', class_='Rating__text').text
                response_marks = rq.get(
                    f'https://vkusvill.ru/ajax/product_comments/from_api/comments_load.php?id={product}')
                soup = bs(response_marks.text, 'html.parser')
                marks_morning = [i.text for i in soup.find_all('span', class_='ProductCommentsRating--cnt')]
                result_m.extend(marks_morning)
                result_m.append(avg)
            add_to_gsheet(result_m)
            print('Готово утро')
            counter = 1
            time.sleep(3600)
        elif counter == 1:
            result_e = ['Вечер', datetime.date.today().strftime('%d.%m.%Y')]
            for product in products:
                response_marks = rq.get(
                    f'https://vkusvill.ru/ajax/product_comments/from_api/comments_load.php?id={product}')
                soup = bs(response_marks.text, 'html.parser')
                marks_ev = [i.text for i in soup.find_all('span', class_='ProductCommentsRating--cnt')]
                result_e.extend(marks_ev)
                result_e.append('')
            add_to_gsheet(result_e)
            print('Готово вечер')
            # Считаем разницу между вечерними и утренними данными
            result_diff = [datetime.date.today().strftime('%d.%m.%Y')]
            result_diff.insert(0, 'Разница')
            for i in range(2, 26):
                if '.' not in result_e[i] and result_e[i].isdigit():
                    result_diff.append(int(result_e[i]) - int(result_m[i]))
                else:
                    result_diff.append('')
            print('diff - ', result_diff)
            add_to_gsheet(result_diff)
            print('Готово разница')
            counter = 0
            time.sleep(3600)


if __name__ == '__main__':
    main()
