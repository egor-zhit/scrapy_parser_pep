import re
import scrapy
from pep_parse.items import PepParseItem
from pep_parse.settings import ALLOWED_DOMAINS, PEP_NAME_PATTERN


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = [ALLOWED_DOMAINS]
    start_urls = [f"https://{ALLOWED_DOMAINS}/"]

    def parse(self, response):
        urls_list = response.css('section[id="numerical-index"] tr')
        for url in urls_list:
            pep_url = url.css("td a::attr(href)").get()
            if pep_url is not None:
                yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        full_name = response.css("h1.page-title::text").get()
        pep_name_match = re.search(PEP_NAME_PATTERN, full_name)
        number, name = pep_name_match.groups()
        status = (
            response.css('dt:contains("Status:") + dd').css("abbr::text").get()
        )
        data = {"number": number, "name": name, "status": status}
        yield PepParseItem(data)
