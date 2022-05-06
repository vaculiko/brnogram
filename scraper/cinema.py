from datetime import datetime
from utils import *

# art = "https://www.kinoart.cz/cs/program/cihlarska"
# def parse_datetmie_art(date_time):
#     for info in [d.strip("\t") for d in date_time.splitlines()]:
#         if "." in info:
#             event_date = info
#         elif ":" in info:
#             event_time = info
#     return event_date, event_time
# art_soup = get_soup(art)
# calendar = art_soup.find("div", {"class":"events-calendar"})
# events = calendar.find_all("div", {"class": "events-calendar__event"})

# for event in events:
#     date_time = event.find("p", {"class": "events-calendar__event-time"}).text
#     event_date, event_time = parse_datetmie_art(date_time)

#     name_link = event.find("h3", {"class": "events-calendar__event-title"})
#     event_name = name_link.text.strip("\n")
#     event_link = name_link.a["href"]

def filter_price(price):
    if "Kč" in price:
        return price.split(" ")[-1]
    else:
        return price

def filter_name(name):
    return name.split("  ")[0]

def kino_art():
    # get table
    art = "https://www.kinoart.cz/cs/program/seznam"
    art_df = pd.read_html(art, index_col=None)[0].drop(columns=[0,2,3])
    # process columns
    art_df.columns = ["Time", "Name", "Price"]
    # add default values
    art_df["Link"] = art
    art_df["Venue"] = "Kino Art"
    # filter price and event name
    art_df["Price"] = art_df["Price"].apply(filter_price)
    art_df["Name"] = art_df["Name"].apply(filter_name)
    # process time and date, split column and rearrange in for loop
    art_df[["Time", "Date"]] = art_df["Time"].str.split("  ", 1, expand=True)
    date = datetime.now().strftime("%d. %B")
    for idx, row in art_df.iterrows():
        if row["Date"]:
            time = row["Date"]
            date = row["Time"]
            row["Date"] = date
            row["Time"] = time
        else:
            row["Date"] = date
    # rearrange columns
    art_df = art_df[["Date", "Time", "Name", "Venue", "Price", "Link"]]
    return art_df

if __name__ == "__main__":
    df = kino_art()
    df.to_html("art_df.html")