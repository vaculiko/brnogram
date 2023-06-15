from turtle import title
import pandas as pd

from scraper.utils import get_events, init_df, this_year, today_numeric

def artbar():
    artbar_df, row = init_df("Artbar Druhý Pád")
    events = get_events("https://www.artbar2pad.com/shows",
                        "li", {"data-hook": "events-card"})
    for event in events:
        try:
            dmt = event.find("div", {"data-hook": "date"}).text.split(". ")
            if len(dmt) == 3:
                date, month, time = dmt
            else:
                date, month = dmt[:2]
                time = dmt[2].split(" – ")[0]
        except ValueError:
            print("Neco chybi, mam", dmt)
            
        event_datetime = pd.to_datetime(f"{this_year()}-{month}-{date} {time}")
        row["Date"] = event_datetime.date()
        row["Time"] = event_datetime.time()
        title = event.find("div", {"data-hook": "title"})
        row["Name"] = title.text.strip()
        row["Link"] = title.a["href"]
        info = event.find("div", {"data-hook": "description"})
        if info:
            row["Info"] = info.text.replace("\n", " ")
        artbar_df.loc[len(artbar_df.index)] = row
    return artbar_df


def melodka():
    melodka_df, row = init_df("Melodka")
    base_url = "https://www.melodka.cz/program/default/"
    _, month, year = today_numeric()

    for mon in range(month, month + 5):
        events = get_events(f"{base_url}{year}-{mon}",
                             "div", {"class": "program_line2"})
        for event in events:
            date = event.find("div", {"class": "datum"}).text
            # print(date)
            # exit()
            row["Date"] = pd.to_datetime(date, dayfirst=True).date()
            title = event.find("div", {"class": "nazev"})
            row["Name"] = title.text.strip()
            row["Link"] = "https://www.melodka.cz" + title.a["href"]
            melodka_df.loc[len(melodka_df.index)] = row

    return melodka_df

def metro():
    metro_df, row = init_df("Metro Music")
    events = get_events("https://www.metromusic.cz/program/", "div",
                          {"class": "item-inner"})
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

def enter():
    url = "https://www.smsticket.cz/mista/4115-enter-club"
    return smsticket(url, "Enter")

def exit_club():
    url = "https://www.smsticket.cz/mista/1487-exit-club"
    return smsticket(url, "Exit")

def fleda():
    pass

def smsticket(url, venue):
    sms_df, row = init_df(venue)
    events = get_events(url, "div", {"class": "event"})
    for event in events:
        event_start = event.find("div", {"property":"startDate"})["content"]
        event_datetime = pd.to_datetime(event_start, format="%Y-%m-%dT%H:%M:00.0000000Z")
        row["Date"] = event_datetime.date()
        row["Time"] = event_datetime.time()
        row["Name"] = event.find("strong", {"property": "name"}).text.strip()
        row["Link"] = "https://www.smsticket.cz" + event.a["href"]
        row["Price"] = event.find("strong", {"property": "price"})["content"].split('.')[0]
        row["Info"] = event["typeof"]
        sms_df.loc[len(sms_df.index)] = row
    return sms_df


def clubs():
    """Scrape all clubs"""
    df_all = pd.concat([artbar(), melodka(), metro(), enter(), exit_club()])
    df_all = df_all.sort_values(by="Date")
    return df_all
