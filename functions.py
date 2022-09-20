from oauth2client.service_account import ServiceAccountCredentials
import gspread as gs
import requests as rq
from bs4 import BeautifulSoup as bs
import datetime

# Указываем путь к JSON с ключомhe
CREDENTIALS_FILE = '../credentials.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
gc = gs.authorize(credentials)

# Словарь со списком проверяемых товаров {'id': 'url}
products = {'53303': 'https://vkusvill.ru/goods/pitstsa-pepperoni-53303.html',
            '35087': 'https://vkusvill.ru/goods/pitstsa-margarita-400-g-ays-35087.html',
            '36161': 'https://vkusvill.ru/goods/pitstsa-mini-s-vetchinoy-i-syrom-zamorozhennaya-36161.html',
            '37523': 'https://vkusvill.ru/goods/pitstsa-s-vetchinoy-kurinoy-i-syrom-37523.html'
            }

today = datetime.date.today().strftime('%d.%m.%Y')
result_m = ['Утро', today]
result_e = ['Вечер', today]


# Функция добавления строки с показателями в Google Sheet
def add_to_gsheet(result):
    wks = gc.open('Sheets-1').worksheet(result[1][3:])
    wks.append_row(result)
    print('Готово', result[0])


# Функция сбора данных с сайта
def parse_marks(products, result):
    for product in products:
        response_avg = rq.get(products[product])
        soup_avg = bs(response_avg.text, 'html.parser')
        avg = soup_avg.find('div', class_='Rating__text').text
        response_marks = rq.get(
            f'https://vkusvill.ru/ajax/product_comments/from_api/comments_load.php?id={product}')
        soup = bs(response_marks.text, 'html.parser')
        marks = [i.text for i in soup.find_all('span', class_='ProductCommentsRating--cnt')]
        result.extend(marks)
        result.append(avg)
    return result

