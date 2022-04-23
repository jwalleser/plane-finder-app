from bs4 import BeautifulSoup

def read_html_into_soup(html_file):
    with open(html_file) as f:
        html = f.read()
    soup = BeautifulSoup(html, features='html.parser')
    return soup
