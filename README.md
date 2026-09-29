# GoIT Web Homework 9

Scraping `quotes.toscrape.com` with Scrapy.

## Main command

```powershell
python main.py
```

The scraper creates:

- `quotes.json`
- `qoutes.json`
- `authors.json`

## MongoDB import

After scraping:

```powershell
python seed_quotes.py
```

## Previous homework search

```powershell
python search_quotes.py
```

Example commands:

```text
name:Albert Einstein
name:st
tag:life
tags:life,live
exit
```

Before running MongoDB-related scripts, create `.env` from `.env.example` and put your MongoDB URI there.
