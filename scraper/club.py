import pandas as pd
from utils import get_soup, df_columns, df_row

def artbar():
    artbar_soup = get_soup("https://www.artbar2pad.com/shows")
    artbar_df = pd.DataFrame(columns=df_columns, index=None)
    row = df_row.copy()
    row["Venue"] = "Artbar Druhý Pád"
    row["Price"] = None

    events = artbar_soup.find_all("li", {"data-hook":"events-card"})
    for event in events:
        date_time = event.find("div", {"data-hook": "date"}).text
        row["Date"] = date_time[:-6]
        row["Time"] = date_time[-5:]
        row["Name"] = event.find("div", {"data-hook": "title"}).text
        row["Link"] = event.find("div", {"data-hook": "title"}).a["href"]
        row["Info"] = event.find("div", {"data-hook": "description"}).text
        artbar_df.loc[len(artbar_df.index)] = row
    return artbar_df


    