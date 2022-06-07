import json
from pprint import pprint

import pandas as pd
from requests import get

from secret import maps_key

api_url = "https://maps.googleapis.com/maps/api/place/"

venue_names = ["Fléda", "Melodka", "Colabs", "Artbar druhý pád", "Metro music club"]
venue_df_columns = [
    "VenueName", "VenueLink", "VenueAddress", "VenueGPS", "VenueType", "VenuePhone",
    "OpeningHours"
]
api_dict_keys = [
    "name", "website", "formatted_address", "geometry", "types", "formatted_phone_number",
    "opening_hours"
]
# gps - geometry: location

def get_from_api(url):
    response = get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"ERROR - {url}")


def place_details(place_id, fields=[]):
    parameters = f"place_id={place_id}&key={maps_key}&language=cs"
    if fields:
        parameters += f"&fields={",".join(fields)}"
    url = api_url + f"details/json?{parameters}"
    return get_from_api(url)["result"]


def find_place(place_name):
    parameters = f"input={place_name}&inputtype=textquery&key={maps_key}"
    url = api_url + f"findplacefromtext/json?{parameters}"
    return get_from_api(url)["candidates"][0]["place_id"]


if __name__ == "__main__":
    venues_df = pd.DataFrame(columns=venue_df_columns, index=None)
    df_row = {column: None for column in venue_df_columns}
    for venue in venue_names:
        details = place_details(find_place(venue), api_dict_keys)
        # pprint(details)
        for column, key in zip(venue_df_columns, api_dict_keys):
            if key == "geometry":
                df_row[column] = details.get(key)["location"]
            elif key == "opening_hours" and details.get(key):
                df_row[column] = details.get(key)["periods"]
            else:
                df_row[column] = details.get(key)
            pprint(df_row)
        venues_df.loc[len(venues_df.index)] = df_row
    print(venues_df)
    venues_df.to_csv("out/venues.csv", index=False)
    print("Venues df saved to csv.")