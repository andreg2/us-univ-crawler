from playwright.async_api import async_playwright
from ...db.db_connector import DB_CLIENT

import scrapy

class HarvardSpider(scrapy.Spider):
    name = "harvard"

    def start_requests(self):
        urls = [
            "https://www.harvard.edu/programs/?degree_levels=undergraduate"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def split_degrees_str(self, degrees_str):
        if "\n" in degrees_str: return degrees_str.split("\n")
        else: return degrees_str.split()

    async def parse(self, response):
        async with async_playwright() as pw:
            data = []
            browser = await pw.chromium.launch()
            page = await browser.new_page()
            await page.goto(response.url)

            while True:
                elements = await page.query_selector_all(".records__record__c-programs-item___bB7Yx")
                for element in elements:
                    degree_name_node = await element.query_selector(".records__record___PbPhG")
                    degree_name = await degree_name_node.inner_text()
                    
                    data.append(('Harvard University', 'harvard', degree_name))

                next_button = await page.query_selector(".c-pagination__link--next")

                if next_button is None: break
                else: await next_button.click()
            
            db = DB_CLIENT("univs.db")
            db.execute_many_inserts("INSERT INTO programs VALUES(?, ?, ?)", data)                