from ...db.db_connector import DB_CLIENT

import scrapy

class YaleSpider(scrapy.Spider):
    name = "yale"

    start_urls = ["https://www.yale.edu/academics/departments-programs"]

    def parse(self, response):
        programs = response.css(".department_item_link::text").getall()
        data = [("Yale University", "yale", program) for program in programs]

        db = DB_CLIENT("univs.db")
        db.execute_many_inserts("INSERT INTO programs VALUES(?, ?, ?)", data)
