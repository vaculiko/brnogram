# brnogram

Program akcí ve vybraných podnicích z Brna na jednom místě!  
Zatím jako tabulkový výpis času, názvu a odkazu na stránky akce.

➡️ https://brnogram.pythonanywhere.com/home ⬅️

## 💻 Aktuální implementace

1. Scraping přes [`BeautifulSoup`](https://beautiful-soup-4.readthedocs.io/en/latest/)
2. Export do `.csv`, upload na [pythonanywhere](https://www.pythonanywhere.com/)
3. Flask web s rozhraním [`PyWebIO`](https://www.pyweb.io/)

## 💾 Struktura databáze

Aktuální sloupce
```python
["Date", "Time", "Name", "Venue", "Price", "Link", "Info"]
```

Plánované sloupce
```python
events = ["EventStart", "EventEnd", "EventName", "EventPrice", "EventLink", "EventInfo", "VenueName"]
venues = ["VenueName", "VenueLink", "VenueLocation", "VenueType", "VenuePhone", "OpeningHours"]
```

## 📌 Plánované funkce

- Sjednotit datum a čas do sloupce *EventStart*
- Databáze na ukládání výsledků - SQL, nebo něco jiného?
- Automatizovat scraping
- Rozšířit počet podniků
- Filtrování výsledků - místo, čas

## 💡 Nápady do budoucna

- Tlačítko Přidat do kalendáře - `.ical` soubor?
- Mobilní a desktopová verze webu
- Tagy k typu akce - koncert, divadlo, výstava,...
- Filtrování podle typu akce
- Vykreslení akcí na mapě - sloupec `VenueLocation`, datový typ pro GPS souřadnice?
- Info o podniku z Google Maps - [Places API](https://developers.google.com/maps/documentation/places/web-service/details)
- Vlastní API - komunikace s ESP32, M5Paper, Home Assistant,...
=======

Program akcí ve vybraných podnicích z Brna na jednom místě!

## Verze 1

Python scraping do pandas datafrane
Django website na zobraznení dataframe.to_html
Program po týdnu, rozdělení na dny

## Verze 2

Python scraping do databáze (MySQL?)
Django website, zobrazení s filtrováním
Tagy na typy akcí, žánry,...

## Řádek databáze

Date | Hour | Name | Venue | Price | URL
-|-|-|-|-|-
Mon 1.2.2000 | 20:00 | The Show | Scala | 123 | www.scala.cz

### Resources

- Databáze - [Pandas](https://pandas.pydata.org/docs/)
- Scraping - [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/)
- Website - [Django](https://tutorial.djangogirls.org/cs/)
- Hosting - [PythonAnywhere](https://www.pythonanywhere.com/)
