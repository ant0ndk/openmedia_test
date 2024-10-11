import requests
from bs4 import BeautifulSoup


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    h1_count = len(soup.find_all('h1'))
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))
    links = [a['href'] for a in soup.find_all('a', href=True)]

    return {
        'h1_count': h1_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'links': links
    }
