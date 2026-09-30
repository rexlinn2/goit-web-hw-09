import json
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.quotes = []

        self.authors = {}

    def parse(self, response):
        for quote in response.css("div.quote"):
            quote_text = quote.css("span.text::text").get()
            author_name = quote.css("small.author::text").get()
            author_url = quote.css("small.author + a::attr(href)").get()
            tags = quote.css("div.tags a.tag::text").getall()

            self.quotes.append({
                "tags": tags,
                "author": author_name,
                "quote": quote_text,
            })

            full_author_url = (
                response.urljoin(author_url)
                if author_url
                else None
            )

            if author_name and author_name not in self.authors:
                self.authors[author_name] = {
                    "fullname": author_name,
                    "born_date": "",
                    "born_location": "",
                    "description": "",
                }

                if full_author_url:
                    yield response.follow(
                        full_author_url,
                        callback=self.parse_author,
                        meta={"author_name": author_name},
                    )

        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        author_name = response.meta.get("author_name")

        if not author_name or author_name not in self.authors:
            return

        self.authors[author_name]["born_date"] = (
            response.css("span.author-born-date::text").get("") or ""
        ).strip()

        self.authors[author_name]["born_location"] = (
            response.css("span.author-born-location::text").get("") or ""
        ).strip()

        self.authors[author_name]["description"] = (
            response.css("div.author-description::text").get("") or ""
        ).strip()

    def closed(self, reason):
        base_path = Path(__file__).resolve().parent

        authors = list(self.authors.values())

        with open(
            base_path / "authors.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                authors,
                file,
                ensure_ascii=False,
                indent=4,
            )

        with open(
            base_path / "quotes.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.quotes,
                file,
                ensure_ascii=False,
                indent=4,
            )

        with open(
            base_path / "qoutes.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.quotes,
                file,
                ensure_ascii=False,
                indent=4,
            )

        print()
        print("=" * 50)
        print("СКРАПІНГ ЗАВЕРШЕНО")
        print("=" * 50)
        print(f"Цитат зібрано: {len(self.quotes)}")
        print(f"Авторів зібрано: {len(authors)}")
        print("Створено: quotes.json, qoutes.json, authors.json")
        print("=" * 50)


def main():
    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",
            "USER_AGENT": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0 Safari/537.36"
            ),
        }
    )

    process.crawl(QuotesSpider)

    process.start()


if __name__ == "__main__":
    main()