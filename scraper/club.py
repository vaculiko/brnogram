import pandas as pd
from utils import get_soup, df_columns, df_row, this_year, today_numeric

def artbar():
    artbar_df = pd.DataFrame(columns=df_columns, index=None)
    row = df_row.copy()
    row["Venue"] = "Artbar Druhý Pád"

    artbar_soup = get_soup("https://www.artbar2pad.com/shows")
    events = artbar_soup.find_all("li", {"data-hook":"events-card"})
    for event in events:
        date_time = event.find("div", {"data-hook": "date"}).text
        row["Date"] = date_time[:-6] + f" {this_year()}"
        row["Time"] = date_time[-5:]
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
            row["Date"] = event.find("div", {"class": "datum"}).text
            title = event.find("div", {"class": "nazev"})
            row["Name"] = title.text
            row["Link"] = "https://www.melodka.cz" + title.a["href"]
            melodka_df.loc[len(melodka_df.index)] = row
            
    return melodka_df

if __name__ == "__main__":
    # print(artbar())
    # print(melodka())
    df_all = artbar().append(melodka())
    df_all = df_all.sort_index()[["Date", "Name", "Link", "Info"]]
    print(df_all)
    df_all.to_html("out/all.html")
    # melodka().to_markdown("out/melodka.md")
    # artbar().to_markdown("out/artbar.md")
