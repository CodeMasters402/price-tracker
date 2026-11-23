"""
Price tracker (demo).

Fetches the current price of a list of product URLs, appends a
timestamped row for each one to prices.csv, and reports which prices
changed since the previous run.

The demo list uses book pages from https://books.toscrape.com/ — a
practice site made for learning web scraping. Replace PRODUCT_URLS
with your own product pages to track real products.

Run:
    python tracker.py
Run it again later and it will tell you what changed.
"""

import csv
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Demo list: three book pages on the practice site.
PRODUCT_URLS = [
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "https://books.toscrape.com/catalogue/soumission_998/index.html",
]

OUTPUT_FILE = "prices.csv"

HEADERS = {"User-Agent": "CodeMasters-demo-price-tracker/1.0"}


def fetch_price(url):
    """Return (title, price) for one product page."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one("div.product_main h1").get_text(strip=True)
    price = soup.select_one("p.price_color").get_text(strip=True)
    return title, price


def last_known_prices():
    """Read prices.csv and return the most recent price per URL."""
    known = {}
    if not os.path.exists(OUTPUT_FILE):
        return known
    with open(OUTPUT_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            known[row["url"]] = row["price"]
    return known


def main():
    previous = last_known_prices()
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_rows = []

    for url in PRODUCT_URLS:
        title, price = fetch_price(url)
        old_price = previous.get(url)
        if old_price is None:
            print(f"NEW:      {title} — {price}")
        elif old_price != price:
            print(f"CHANGED:  {title} — {old_price} -> {price}")
        else:
            print(f"no change: {title} — {price}")
        new_rows.append(
            {"timestamp": timestamp, "title": title, "url": url, "price": price}
        )

    write_header = not os.path.exists(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "title", "url", "price"]
        )
        if write_header:
            writer.writeheader()
        writer.writerows(new_rows)

    print(f"\nAppended {len(new_rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
