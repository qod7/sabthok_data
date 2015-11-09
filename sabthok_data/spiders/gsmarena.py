import logging
import scrapy

from sabthok_data.items import GsmareanaItem


def read_urls_from_file(filepath):
    """
        Reads starting urls from filepath provided and returns
        a tuple of urls list with names list
    """

    file = open(filepath, "r")
    content = file.read()
    file.close()

    urls = content.split('\n')
    names = []
    for url in urls:
        name = url.split('/')[-1].split('-')[0].split('_')[0]
        names.append(name)

    # Removes duplicates
    names = list(set(names))

    return urls, names


class GsmarenaSpider(scrapy.Spider):
    name = "gsmarena"
    allowed_domains = ["gsmarena.com"]

    # Starting urls
    start_urls, names = read_urls_from_file("gsmarena_urls.txt")

    product_selector = "div.makers > ul > li > a::attr('href')"
    next_page_url_selector = "a.pages-next::attr('href')"

    name_selector = '#body > div > div.review-header.hreview > div > div.article-info-line.page-specs.light.border-bottom > h1::text'
    group_selector = "#specs-list > table"

    def parse(self, response):
        logging.info('Current url ' + response.url)
        for href in response.css(GsmarenaSpider.product_selector):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_product_page)

        # Link for next page
        next_page = response.css(GsmarenaSpider.next_page_url_selector)

        if(next_page):
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_product_page(self, response):
        # Obtain name of product
        name = response.css(GsmarenaSpider.name_selector).extract_first()

        if(not(name)):
            logging.warning("Name not found for url: " + response.url)
            return

        # Create product object
        product = GsmareanaItem(Name=name)

        # Table for category
        specs_groups = response.css(GsmarenaSpider.group_selector)

        for specs_group in specs_groups:
            group_name = specs_group.css('th::text').extract_first()

            rows = specs_group.css('tr')

            properties = {}
            for j, row in enumerate(rows):
                field = row.css('td.ttl > a::text').extract_first()
                value = row.css('td.nfo::text').extract_first()

                if(field == "Technology"):
                    continue

                if(field):
                    properties[field] = value
                else:
                    if('Others' in properties):
                        properties['Others'].append(value)
                    else:
                        properties['Others'] = [value]

            product[group_name] = properties

        return product
