from pprint import pprint

import pandas as pd

from scraper.utils import get_json, get_events, init_df


def colabs():
    colabs_df, row = init_df("CO.LABS")
    # colabs_json = get_json("https://goout.net/services/feeder/v1/events.json?tickets=true&source=buranteatr.cz&contact=1522&language=cs")
    # for event in colabs_json['events'].values():
    # print(event['name'])
    # print(event['tags'])
    # print(event['url'])
    events = get_events("http://www.colabs.cz/program/", "div", {"class": "event-details"})
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

def theatres():
    # df_theatres = pd.concat([colabs()])
    df_theatres = colabs()
    df_theatres = df_theatres.sort_values(by="Date")[["Date", "Name", "Venue", "Link"]]
    return df_theatres
