from tkinter.tix import Tree
import pandas as pd
from utils import get_soup, df_columns, df_row, this_year, today_numeric

def artbar():
    artbar_df = pd.DataFrame(columns=df_columns, index=None)
    row = df_row.copy()
    row["Venue"] = "Artbar Druhý Pád"

    artbar_soup = get_soup("https://www.artbar2pad.com/shows")
    events = artbar_soup.find_all("li", {"data-hook":"events-card"})
    for event in events:
        date, month, time = event.find("div", {"data-hook": "date"}).text.split(".")
        event_datetime = pd.to_datetime(f"{this_year()}-{month}-{date} {time}")
        row["Date"] = event_datetime.date()
        row["Time"] = event_datetime.time()
        title = event.find("div", {"data-hook": "title"})
        row["Name"] = title.text
        row["Link"] = title.a["href"]
        info = event.find("div", {"data-hook": "description"}).text
        row["Info"] = info.replace("\n", " ")
        artbar_df.loc[len(artbar_df.index)] = row
    return artbar_df


def melodka():
    melodka_df = pd.DataFrame(columns=df_columns, index=None)
    row = df_row.copy()
    row["Venue"] = "Melodka"

    base_url = "https://www.melodka.cz/program/default/"
    _, month, year = today_numeric()

    for mon in range(month, month + 5):
        melodka_soup = get_soup(f"{base_url}{year}-{mon}")
        events = melodka_soup.find_all("div", {"class": "program_line2"})

        for event in events:
            date = event.find("div", {"class": "datum"}).text
            # print(date)
            # exit()
            row["Date"] = pd.to_datetime(date, dayfirst=True).date()
            title = event.find("div", {"class": "nazev"})
            row["Name"] = title.text
            row["Link"] = "https://www.melodka.cz" + title.a["href"]
            melodka_df.loc[len(melodka_df.index)] = row

    return melodka_df

def metro():
    metro_df = pd.DataFrame(columns=df_columns)
    row = df_row.copy()
    row["Venue"] = "Metro Music"

    metro_soup = get_soup("https://www.metromusic.cz/program/")
    events = metro_soup.find_all("div", {"class": "item-inner"})
    for event in events:
        date, time = event.find("p", {"class": "date"}).text.strip().split(" ")
        event_datetime = pd.to_datetime(f"{date}/{this_year()}/{time[1:-1]}",
                                        dayfirst=True)
        row["Date"] = event_datetime.date()
        row["Time"] = event_datetime.time()
        row["Name"] = event.find("h3").text.strip()
        row["Link"] = event.a["href"]
        info = event.find("p", {"class": "subhead"})
        if info:
            row["Info"] = info.text.strip()
        metro_df.loc[len(metro_df.index)] = row
        
    return metro_df

def main():
    df_all = pd.concat([artbar(), melodka(), metro()])
    df_all = df_all.sort_values(by="Date")[["Date", "Name", "Venue", "Link"]]
    df_all.to_csv("out/all.csv", index=False)

if __name__ == "__main__":
    # print(metro())
    main()
