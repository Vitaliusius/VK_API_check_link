import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(token, url):
    payload = {
        'access_token': token,
        'v': '5.199',
        'key': urlparse(url).path[1:],
    }
    response = requests.post('https://api.vk.ru/method/utils.getLinkStats', params=payload)
    response.raise_for_status()

    return 'error' not in response.json()


def shorten_link(token, url):
    payload = {
        "access_token": token,
        'v': '5.199',
        'url': url,
    }
    response = requests.post('https://api.vk.ru/method/utils.getShortLink', params=payload)
    response.raise_for_status()

    return response.json()['response']['short_url']


def count_clicks(token, link):
    payload = {
        "access_token": token,
        'v': '5.199',
        'key': link,
        'interval': 'week',
        'intervals_count': 1
    }
    response = requests.post('https://api.vk.ru/method/utils.getLinkStats', params=payload)
    response.raise_for_status()

    return response.json()['response']['stats'][-1]['views']


def main():
    load_dotenv()
    token = os.environ['VK_SERVICE_KEY']
    url = input('Введите ссылку: ')
    try:
        if is_shorten_link(token, url):
            print('Количество кликов: ', count_clicks(token, urlparse(url).path[1:]))
        else:
            print('Короткая ссылка: ', shorten_link(token, url))
    except KeyError:
        print('Ошибка')
    except IndexError:
        print('Количество кликов: 0')
   

if __name__ == '__main__':
    main()
