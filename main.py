import argparse
import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, user_url):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "long_url": user_url
    }
    url = "https://api-ssl.bitly.com/v4/shorten"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["link"]


def is_bitlink(token, user_url ):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    parsed_url = urlparse(user_url)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}/{path}"
    url = url.format(netloc=parsed_url.netloc, path=parsed_url.path)
    response = requests.get(url, headers=headers)
    return response.ok


def count_clicks(token, user_url ):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    parsed_url = urlparse(user_url)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}/{path}/clicks/summary"
    url = url.format(netloc=parsed_url.netloc, path=parsed_url.path)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='Количество преходов по ссылке битли'
    )
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    user_url=args.link
    try:
        if is_bitlink(bitly_token, user_url): 
            print("Количество преходов по ссылке битли: ", count_clicks(bitly_token, user_url))
        else:
            print("Короткая ссылка: ", shorten_link(bitly_token, user_url))
    except requests.exceptions.HTTPError:
        print('ошибка неверная ссылка')
