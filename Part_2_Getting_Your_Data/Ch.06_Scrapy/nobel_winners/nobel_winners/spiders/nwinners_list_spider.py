import scrapy
import re

# Create fields for scraped data using a scrapy item subclass
class NWinnerItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()


# Create named spider using scrapy spider subclass
class NWinnerSpider(scrapy.Spider):
    """ Scrapes the country and link text of the Nobel-winners. """

    name = 'nwinners_list'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        "http://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
    ]

    # Each spider has a parse method which deals with the HTTP requests
    # to a list of start URLs contained in a start_url class attribute
    def parse(self, response):

        h3s = response.xpath('//h3')

        for h3 in h3s:
            country = h3.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h3.xpath('following-sibling::ol[1]')
                for w in winners.xpath('li'):
                    text = w.xpath('descendant-or-self::text()').extract()
                    
                    yield NWinnerItem(
                        country=country[0],
                        name=text[0],
                        link_text = ' '.join(text),
                    )
