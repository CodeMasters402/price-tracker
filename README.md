# Price Tracker

A small price tracker built with `requests` + `BeautifulSoup`. It fetches the current price of a list of product URLs, appends a timestamped row for each one to `prices.csv`, and tells you which prices changed since the previous run.

The demo list uses book pages from [Books to Scrape](https://books.toscrape.com/) — a practice site made for learning web scraping.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python tracker.py
```

Run it again later and it reports what changed:

```
NEW:      A Light in the Attic — £51.77
NEW:      Tipping the Velvet — £53.74
NEW:      Soumission — £50.10

Appended 3 rows to prices.csv
```

Second run, with no price changes:

```
no change: A Light in the Attic — £51.77
no change: Tipping the Velvet — £53.74
no change: Soumission — £50.10

Appended 3 rows to prices.csv
```

## How to add your own URLs

Edit the `PRODUCT_URLS` list at the top of `tracker.py` and put in your own product pages. The tracker reads the product title from `div.product_main h1` and the price from `p.price_color` — if your site uses different selectors, change those two lines in `fetch_price` to match.

## Output

`prices.csv` grows one row per product per run:

```csv
timestamp,title,url,price
2026-11-23T20:10:31+00:00,A Light in the Attic,https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html,£51.77
```

A small sample is committed as `sample_prices.csv`. The full `prices.csv` is ignored by git (see `.gitignore`).

Built by [CodeMasters](https://codemasters402.github.io/) — custom web scrapers, clean Excel/CSV data, fixed quote before starting.
