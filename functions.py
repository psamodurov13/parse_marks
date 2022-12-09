from oauth2client.service_account import ServiceAccountCredentials
import gspread as gs
import requests as rq
from bs4 import BeautifulSoup as bs
import datetime

# Path to JSON with credentials
CREDENTIALS_FILE = '../credentials.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
gc = gs.authorize(credentials)

# Dict with all tracked products {'id': 'url}
products = {'53303': 'https://vkusvill.ru/goods/pitstsa-pepperoni-53303.html',
            '35087': 'https://vkusvill.ru/goods/pitstsa-margarita-400-g-ays-35087.html',
            '36161': 'https://vkusvill.ru/goods/pitstsa-mini-s-vetchinoy-i-syrom-zamorozhennaya-36161.html',
            '37523': 'https://vkusvill.ru/goods/pitstsa-s-vetchinoy-kurinoy-i-syrom-37523.html'
            }

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15'
}

today = datetime.date.today().strftime('%d.%m.%Y')
result_m = ['Утро', today]
result_e = ['Вечер', today]


def add_to_gsheet(result):
    '''
    The function of adding rows with indicators in Google Sheet
    '''
    wks = gc.open('Sheets-1').worksheet(result[1][3:])
    wks.append_row(result)
    print('Done', result[0])


def parse_marks(products, result):
    '''
    The function collect data frow website
    '''
    s = rq.Session()
    for product in products:
        response_avg = s.get(products[product], headers=headers)
        soup_avg = bs(response_avg.text, 'html.parser')
        avg = soup_avg.find('div', class_='Rating__text').text
        print('Average rating: ', avg)
        response_marks = s.get(
            f'https://vkusvill.ru/ajax/product_comments/from_api/comments_load.php?id={product}', headers=headers)
        soup = bs(response_marks.text, 'html.parser')
        marks = [i.text for i in soup.find_all('span', class_='ProductCommentsRating--cnt')]
        result.extend(marks)
        result.append(avg)
        mark = 5
        summa = 0
        counts = 0
        for i in marks:
            summa += int(i) * mark
            counts += int(i)
            mark -= 1
        average = '%.4f' % (summa / counts)
        result.append(average)
    return result

