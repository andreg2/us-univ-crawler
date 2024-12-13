from playwright.async_api import async_playwright
from ...db.db_connector import DB_CLIENT

import scrapy

class THESpider(scrapy.Spider):
    name = "the"

    def start_requests(self):
        urls = [
            "https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    async def parse(self, response):
        async with async_playwright() as pw:
            data = []
            browser = await pw.chromium.launch()
            page = await browser.new_page()
            await page.goto(response.url)

            for _ in range(4):
                elements = await page.query_selector_all("table#datatable-1 tbody tr")
                for element in elements:
                    ranking_node = await element.query_selector("td.rank")
                    university_name_node = await element.query_selector("td.name a.ranking-institution-title")
                    univeristy_name = await university_name_node.inner_text()
                    ranking = await ranking_node.inner_text()
                    
                    data.append((univeristy_name, ranking, "THE"))

                next_button = await page.query_selector("li#datatable-1_next a[href='/world-university-rankings/latest/world-ranking']")
                print(next_button)
                await next_button.click()
            print(data)
            # db = DB_CLIENT("univs.db")
            # db.execute_many_inserts("INSERT INTO rankings VALUES(?, ?, ?)", data)   