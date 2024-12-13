from playwright.async_api import async_playwright
from ...db.db_connector import DB_CLIENT

import scrapy

class ShanghaiSpider(scrapy.Spider):
    name = "shanghai"

    def start_requests(self):
        urls = [
            "https://www.shanghairanking.com/institution"
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
                elements = await page.query_selector_all("div.univ-container div.univ-main")

                for element in elements:
                    ranking_node = await element.query_selector("div.rank-box span:nth-child(2)")
                    university_name_node = await element.query_selector("div.school-container div.univ-container span.univ-name")
                    univeristy_name = await university_name_node.inner_text()
                    ranking = await ranking_node.inner_text()
                    
                    data.append((univeristy_name, ranking, "shanghai"))

                next_button = await page.query_selector("li.ant-pagination-next a.ant-pagination-item-link")
                await next_button.click()

            db = DB_CLIENT("univs.db")
            db.execute_many_inserts("INSERT INTO rankings VALUES(?, ?, ?)", data)   