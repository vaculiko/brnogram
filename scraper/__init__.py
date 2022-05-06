import pandas as pd

from scraper.cinema import cinemas
from scraper.club import clubs, melodka
from scraper.theatre import theatres, colabs


def test():
    print(theatres())


def run():
    print("Spoustim scraping")
    df_all = pd.concat([clubs(), theatres()])
    df_all = df_all.sort_values(by="Date")[["Date", "Name", "Venue", "Link"]]
    df_all.to_csv("out/all.csv", index=False)