from pprint import pprint

import pandas as pd

from scraper.utils import get_json, get_events, init_df, this_year, this_month


def colabs():
    colabs_df, row = init_df("CO.LABS")
    urls = [
        "http://www.colabs.cz/program/?categoryIds%5B0%5D=1",
        # "https://colabs.cz/program/?categoryIds%5B0%5D=3",
        # "https://colabs.cz/program/?categoryIds%5B0%5D=2"
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
            category = event.find("div", {"class": "event-category-price"})
            if category:
                category_text = category.text.split("//")[1].strip()
                row["Info"] = category_text.strip()
            price = event.find("div", {"class": "event-buy-tickets"})
            if price:
                row["Price"] = price.text.split(" ")[2]
            colabs_df.loc[len(colabs_df.index)] = row

    return colabs_df


def kjogen():
    kjogen_df, row = init_df("Kjógen")
    urls = [f"http://www.kjogen.cz/{this_year()}/{m}/" for m in range(1, 13)]
    for url in urls:
        # print(url)
        table = get_events(url, "table", {"class": "program"})
        if table:
            for trow in table[0].find("tbody").find_all("tr"):
                date_time, venue_info, program = trow.find_all("td")
                day, date, time = date_time.get_text(strip=True, separator='\n').splitlines()
                if "Brno" in venue_info.text:
                    city, row["Venue"], address = venue_info.get_text(strip=True, separator='\n').splitlines()
                    row["Name"]= program.get_text(strip=True, separator=', ').replace(", VSTUPENKY", "")
                    event_datetime = pd.to_datetime(date + time, format="%d.%m.%Y%H:%M")
                    row["Date"] = event_datetime.date()
                    row["Time"] = event_datetime.time()
                    if program.find("a"):
                        row["Link"] = program.find("a")["href"]
                    kjogen_df.loc[len(kjogen_df.index)] = row
    
    return kjogen_df

def theatres():
    df_theatres = pd.concat([colabs(), kjogen()])
    # df_theatres = colabs()
    df_theatres = df_theatres.sort_values(by="Date")
    return df_theatres


if __name__ == "__main__":
    kjogen()