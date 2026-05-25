from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://www.goo-net.com/usedcar/brand-NISSAN/car-GT-R/"
HEADERS ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
logging.basicConfig(level=logging.INFO)


@dataclass
class CarListing:
    title: str
    price: str
    dealer: str

def fetch_page(URL: str) -> str:
     #download page html safely
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    response.encoding = response.apparent_encoding
    logging.info("Status: %s", response.status_code)

    return response.text 

def parse_listings(html: str) -> List[CarListing]:
    #Extract car listings from page HTML
    soup = BeautifulSoup(html, "html.parser")
    
    #print(len(soup.text))
    cars = soup.find_all("div",class_="data")
    logging.info("Listings found: %d",len(cars))
    listings: List[carListing] = []

    for car in cars:
        title_elem = car.select_one("p.ttl")
        title = title_elem.get_text(strip=True) if title_elem else "N/A"
        price_elem = car.select_one(".num-red")
        price = price_elem.get_text(strip=True) if price_elem else "N/A"
        dealer_elem = car.select_one(".shop")
        dealer = dealer_elem.get_text(strip=True) if dealer_elem else "N/A"
        
        listings.append(
            CarListing(
            title=title,
            price=price,
            dealer=dealer,)
        )
    return listings

def export_to_dataframe(listings: List[CarListing]) -> pd.DataFrame:
    #Convert listings to pandas DataFrame
    return pd.DataFrame(asdict(car) for car in listings)
    """print("TITLE:",title if title else "N/A")
    print("PRICE:", price if price else "N/A")
    print("DEALER:", dealer.text.strip() if dealer else "N/A")
    print("-" * 40)"""

def main() -> None:
    html = fetch_page(URL)
    listings = parse_listings(html)
    df = export_to_dataframe(listings)
    print(df.head())
 

if __name__=='__main__':
    main()






