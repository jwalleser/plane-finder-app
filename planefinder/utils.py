from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup


def read_html_into_soup(html_file):
    if is_http(html_file):
        html = get_webpage(html_file)
    else:
        with urlopen(html_file) as f:
            html = f.read()
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def get_webpage(address):
    response = requests.get(address)
    return response.text


def is_http(path: str) -> bool:
    return str(path).lower().startswith("http")
