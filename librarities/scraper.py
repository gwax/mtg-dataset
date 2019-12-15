"""Scraper for magic librarities english card information."""

import datetime as dt
from typing import Any, Dict, Generator, Optional

from parsel.selector import Selector
from scrapy.http import TextResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

DATE_FORMATS = [
    # (length, format)
    (10, "%Y-%m-%d"),
    (7, "%Y-%m"),
    (4, "%Y"),
]


def parse_card_date(datestr: str) -> Optional[dt.date]:
    """Attempt multiple date formats to convert from DATE to date()."""
    for length, date_format in DATE_FORMATS:
        try:
            return dt.datetime.strptime(datestr[:length], date_format).date()
        except ValueError:
            pass
    return None


class MagicLibraritiesSpider(CrawlSpider):
    """Scrapy spider for extracting cards from Magic Librarities."""

    name = "librarities"
    allowed_domains = ["magiclibrarities.net"]
    start_urls = ["https://www.magiclibrarities.net/rarities.html"]
    rules = [
        Rule(
            LinkExtractor(allow=[r".*-english-cards-index\.html$"]),
            callback="parse_set",
        )
    ]

    @staticmethod
    def parse_set(response: TextResponse) -> Generator[Dict[str, Any], None, None]:
        """Parse a set page into individual cards."""
        set_name = response.xpath('//span[@class="t12g"]/text()').get()
        set_tables = response.xpath('//tr[@class="tabeg"]/..')
        for table in set_tables:
            set_category = table.xpath("preceding-sibling::a//text()").get()
            rows = table.xpath(".//tr")
            header, *rows = rows
            column_names = [
                c.xpath("string()").get(default=f"UNK{i:03d}")
                for i, c in enumerate(header.xpath("td"))
            ]
            for row in rows:
                cells = [get_cell_text(c) for c in row.xpath("td")]
                card = dict(zip(column_names, cells))
                if not card.get("CARDNAME"):
                    continue
                release_date = parse_card_date(card.get("DATE", ""))
                card["set_name"] = set_name
                card["set_category"] = set_category
                card["release_date"] = "" if release_date is None else str(release_date)
                yield card


def get_cell_text(cell: Selector) -> str:
    """Extract text elements from a cell, strip whitespace, and join by line break."""
    vals = (text.get().strip() for text in cell.xpath(".//text()"))
    vals = (v for v in vals if v)
    return "\n".join(vals)
