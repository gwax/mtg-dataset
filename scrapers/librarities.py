"""Scraper for magic librariteis english card information."""

import datetime as dt
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

DATE_FORMATS = [
    # (length, format)
    (10, "%Y-%m-%d"),
    (7, "%Y-%m"),
    (4, "%Y"),
]


def parse_card_date(datestr):
    """Attempt multiple date formats to convert from DATE to date()."""
    for length, date_format in DATE_FORMATS:
        try:
            return dt.datetime.strptime(datestr[:length], date_format).date()
        except ValueError:
            pass
    return None


class MagicLibraritiesSpider(CrawlSpider):
    """Scrapy spider for extacting cards from Magic Librarities."""

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
    def parse_set(response):
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
                card["set_name"] = set_name
                card["set_category"] = set_category
                card["release_date"] = parse_card_date(card.get("DATE", ""))
                yield card


def get_cell_text(cell):
    """Extract text elements from a cell, strip whitespace, and join by linebreak."""
    vals = (text.get().strip() for text in cell.xpath('.//text()'))
    vals = (v for v in vals if v)
    return '\n'.join(vals)
