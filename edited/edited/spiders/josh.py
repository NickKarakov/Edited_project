import scrapy
from scrapy_playwright.page import PageCoroutine


class JoshSpider(scrapy.Spider):
    name = 'josh'

    def start_requests(self):
        yield scrapy.Request('https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99',
                             meta=dict(
                                 playwright=True,
                                 playwright_include_page=True,
                                 playwright_page_coroutines=[
                                     PageCoroutine('wait_for_selector', 'div.product-actions')
                                 ]

                             ))

    async def parse(self, response):

        sizes = []
        for size in response.css('span.size-unavailable::text'):
            sizes.append(size.get()[:2])

        yield {
            'name': response.css('h1::text').get(),
            'current_price': float(response.css('span.product-sale.product-sale--discount::text').get().replace('£', '')),
            'color': response.css('span.colors-info-name::text').get(),
            'sizes': sizes,
        }
