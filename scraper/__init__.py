import pandas as pd

from scraper.cinema import cinemas
from scraper.club import clubs, melodka
from scraper.theatre import theatres, colabs


def test():
    print(theatres())

def run(filtering=True):
    print("--- Spoustim scraping ---")
    df_all = pd.concat([clubs(), theatres()])
    # select only some columns
    if filtering:
        df_all= df_all[["Date", "Name", "Venue", "Link"]]
    return df_all.sort_values(by="Date")
    
def all_to_csv():
    df_all = run()
    df_all.to_csv("out/all.csv", index=False)
    print("--- Ulozeno do 'out/all.csv' ---")
    
def all_to_sql():
    df_all = run()