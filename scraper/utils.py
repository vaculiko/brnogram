import json
from datetime import datetime

import pandas as pd
from requests import get, post
from bs4 import BeautifulSoup

df_columns = ["Date", "Time", "Name", "Venue", "Price", "Link", "Info"] # doplnit z Dell
df_row = {column:None for column in df_columns}

def init_df(venue_name):
    df = pd.DataFrame(columns=df_columns, index=None)
    row = df_row.copy()
    row["Venue"] = venue_name
    return df, row

def get_soup(url: str) -> BeautifulSoup:
    response = get(url)
    if response.status_code == 200:
        print(f"OK - {url}")
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"ERROR - {url}")
    

def get_events(url: str, tag: str, attrs: dict):
    soup = get_soup(url)
    if soup:
        return soup.find_all(tag, attrs)  

def post_soup(url: str, payload):
    response = post(url, data=payload)
    if response.status_code == 200:
        print(f"OK - {url}")
    else:
        print(f"ERROR - {url}")
    return BeautifulSoup(response.text, 'html.parser')

def get_json(url: str):
    response = get(url)
    if response.status_code == 200:
        print(f"OK - {url}")
    else:
        print(f"ERROR - {url}")
    return json.loads(response.text)


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