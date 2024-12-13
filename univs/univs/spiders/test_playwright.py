import scrapy

class PlaywrightSpider(scrapy.Spider):
    name = "playwright"

    start_urls = ["https://majors.stanford.edu/majors"]

    def parse_degree_url(self, degree_path):
        return "https://majors.stanford.edu" + degree_path
    
    def parse_major(self, response):
        majors = response.xpath('//*[contains(text(), "Degrees Offered")]/following-sibling::*[1]/li/text()')
        print(majors.extract())
    
    def parse(self, response):
        major_paths = response.css("li section h2 a::attr(href)").getall()
        degree_urls = [self.parse_degree_url(major_path) for major_path in major_paths]
        
        for url in degree_urls:
            yield scrapy.Request(url=url, callback=self.parse_major)