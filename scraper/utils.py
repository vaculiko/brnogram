from datetime import datetime

from requests import get, post
from bs4 import BeautifulSoup

df_columns = ["Date", "Time", "Name", "Venue", "Price", "Link", "Info"] # doplnit z Dell
df_row = {column:None for column in df_columns}

def get_soup(url: str):
    response = get(url)
    if response.status_code == 200:
        print(f"OK - {url}")
    else:
        print(f"ERROR - {url}")
    return BeautifulSoup(response.text, 'html.parser')

def post_soup(url: str, payload):
    response = post(url, data=payload)
    if response.status_code == 200:
        print(f"OK - {url}")
    else:
        print(f"ERROR - {url}")
    return BeautifulSoup(response.text, 'html.parser')


def today_numeric() -> tuple:
    """Returns tuple (d, m, y) of today's date as integers."""
    d, m, y = datetime.now().strftime("%d-%m-%Y").split("-")
    return (int(d), int(m), int(y))

def this_month() -> int:
    return today_numeric()[1]


def this_year() -> int:
    return today_numeric()[2]

if __name__ == "__main__":
    print(today_numeric())