from pprint import pprint

import pandas as pd

from scraper.utils import get_json, get_events, init_df, this_year, this_month


def colabs():
    colabs_df, row = init_df("CO.LABS")
    urls = [
        "https://colabs.cz/program/?categoryIds%5B0%5D=1",
        "https://colabs.cz/program/?categoryIds%5B0%5D=3",
        "https://colabs.cz/program/?categoryIds%5B0%5D=2"
    ]
    for url in urls:
        events = get_events(url, "div", {"class": "event-details"})
        for event in events:
            event_date = event.find("div", {"class": "event-date"})
            if event_date:
                event_datetime = pd.to_datetime(event_date.text.strip(),
                                                format="%d / %m / %Y ~ %H / %M")
                row["Date"] = event_datetime.date()
                row["Time"] = event_datetime.time()
            else:
                continue
            title = event.find("div", {"class": "event-title"})
            row["Name"] = title.text.strip()
            row["Link"] = "http://www.colabs.cz" + title.a["href"]
            category_price = event.find("div", {"class": "event-category-price"})
            if category_price:
                _, category, price = category_price.text.split("//")
                row["Info"] = category.strip()
                if price:
                    row["Price"] = price.replace(",-", "").strip()
            colabs_df.loc[len(colabs_df.index)] = row

    return colabs_df


def kjogen():
    kjogen_df, row = init_df("Kjógen")
    urls = [f"http://www.kjogen.cz/{this_year()}/{m}/" for m in range(1, 13)]
    for url in urls:
        # print(url)
        table = get_events(url, "table", {"class": "program"})
        if table:
            for row in table[0].find("tbody").find_all("tr"):
                date_time, venue, program = row.find_all("td")
                print(date_time.text, venue.text, program, sep="\n", end="\n\n")

def theatres():
    # df_theatres = pd.concat([colabs()])
    df_theatres = colabs()
    df_theatres = df_theatres.sort_values(by="Date")[["Date", "Name", "Venue", "Link"]]
    return df_theatres


if __name__ == "__main__":
    kjogen()