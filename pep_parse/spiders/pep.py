import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css(
            'section[id=numerical-index] tbody a::attr(href)'
        )
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):

        pep = response.css('.page-title::text').get().split()
        pep_number = pep[1]
        pep_name = ' '.join(pep[3:])
        pep_status = response.css('abbr::text').get()

        data = {
            'number': pep_number,
            'name': pep_name,
            'status': pep_status
        }
        yield PepParseItem(data)
