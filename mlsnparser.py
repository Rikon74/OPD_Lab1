import requests
from bs4 import BeautifulSoup
import pandas
from fake_useragent import UserAgent


def comment(a, i, data):  # формирует нормальный комментарий
    comm = ''
    count = 0
    for txt in a:
        if count % 2 == 1:
            for txtdivision in txt:
                comm += txtdivision.text + ' '
        count += 1
    data['description'][i] += (comm.replace('\xa0', ' '))
    i += 1
    return i


def parser(url):
    try:
        page = requests.get(url, headers={'UsAg': UserAgent().chrome})
        bf_soup = BeautifulSoup(page.text, "html.parser")
        location_parser = bf_soup.findAll('a', class_='location slim')
        price_parser = bf_soup.findAll('div', class_='property__price')
        area_parser = bf_soup.findAll('div', class_='property__area')
        level_parser = bf_soup.findAll('div', class_='property__building')
        data = {'price': [], 'location': [], 'type': [], 'level': [], 'area': [], 'description': [], 'urls': []}

        for link in location_parser:
            data['urls'].append(link.get('href'))  # находит ссылку на объявление
            data['location'].append(link.contents[1])  # находит адрес
            data['type'].append(link.find('span', class_='main-param').contents[0])  # находит тип жилья

        for price in price_parser:
            comm = ''
            count = 0
            for txt in price:
                if count % 2 == 1:
                    comm += txt.text + " "  # формирует элементы в словаре для ключа description
                count += 1
            data['description'].append(comm.replace('\xa0', ' '))
            data['price'].append(price.find('span', class_='main-param').text.replace('\xa0', ''))  # находит цену

        i = 0
        for level in level_parser:
            a = level
            i = comment(a, i, data)
            data['level'].append(level.find('span', class_='main-param').text.replace('Этаж: ', ''))

        i = 0
        for area in area_parser:
            a = area
            i = comment(a, i, data)
            if area.find('span', class_='main-param') is None:  # находит объявления, где не указана площадь
                data['area'].append('Не указана')
                continue
            data['area'].append(area.find('span', class_='main-param').text.replace('\xa0', ''))  # находит площадь
        pandas.DataFrame(data).to_excel('parser.xlsx')
    except:
        print('Ошибка')
