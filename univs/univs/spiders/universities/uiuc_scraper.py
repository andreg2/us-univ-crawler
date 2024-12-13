from ...db.db_connector import DB_CLIENT

import scrapy

class UiucSpider(scrapy.Spider):
    name = "uiuc"

    start_urls = ["http://catalog.illinois.edu/courses-of-instruction/"]

    def parse(self, response):
        data = []
        programs = response.css("div#atozindex li a::text").getall()
        for program in programs:
            filtered_program = program.split("- ")[1]
            data.append(("University of Illinois at Urbana-Champaign", "uiuc", filtered_program))
        
        db = DB_CLIENT("univs.db")
        db.execute_many_inserts("INSERT INTO programs VALUES(?, ?, ?)", data)