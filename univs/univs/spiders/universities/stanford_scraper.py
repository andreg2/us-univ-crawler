from ...db.db_connector import DB_CLIENT

import scrapy

class HarvardSpider(scrapy.Spider):
    name = "stanford"

    start_urls = ["https://majors.stanford.edu/majors"]

    def parse(self, response):
        programs = response.css("li div.su-card__contents h3.su-card__link a::text").getall()
        data = [("Stanford University", "stanford", program) for program in programs]

        db = DB_CLIENT("univs.db")
        db.execute_many_inserts("INSERT INTO programs VALUES(?, ?, ?)", data)