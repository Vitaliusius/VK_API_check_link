import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def check_shorten_link(token, url):
    payload = {
        'access_token': token,
        'v': '5.199',
        'key': urlparse(url).path[1:],
        'interval': 'week',
        'intervals_count': 1
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

    return response.json()


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

    return response.json()

    try:
        clicks_count = response.json()['response']['short_url']['views']
    except KeyError:
        return ("Ошибка", response.json()["error"])
    else:
        return clicks_count


def main():
    load_dotenv()
    token = os.environ['VK_SERVICE_KEY']
    url = input('Введите ссылку: ')

    if check_shorten_link(token, url):
        print('Колличество кликов: ', count_clicks(token, urlparse(url).path[1:])['response']['stats'][-1]['views'])
    else:
        try:
            print('Короткая ссылка: ', shorten_link(token, url)['response']['short_url'])
        except KeyError:
            print("Ошибка", shorten_link(token, url)['error'])


if __name__ == '__main__':
    main()
