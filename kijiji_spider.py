import scrapy
from scrapy.crawler import CrawlerProcess


class Playbook(scrapy.Spider):
    name = "PostcodesSpider"

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'BikesFinal.csv',
    }

    def start_requests(self):
        for i in range(1, 30):
            yield scrapy.Request(url="https://www.kijiji.ca/b-motorcycles/alberta/page-" + str(i) + "/c30l9003",
                                    callback=self.parse, dont_filter=True,
                                    headers={
                                         'USER-AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                                    },
                                 )




    def parse(self, response):
        urls = response.css("div.title > a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request("https://www.kijiji.ca" + url,
                                 callback=self.parse2, dont_filter=True,
                                 headers={
                                     'USER-AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                                 },
                                 )






    def parse2(self, response):
        name = response.css("h1.title-2323565163::text").extract_first()
        data1 = response.css("ul.itemAttributeList-1090551278 > li")
        data2 = response.css("ul.itemAttributeList-1090551278:nth-of-type(2) > li")

        data1.append(data2)

        model = "N/A"
        color = "N/A"
        engn = "N/A"
        year = "N/A"
        make = "N/A"
        km = "N/A"
        for d in data1:

            print(d.css("dt::text").extract_first())
            if "Make" == d.css("dt::text").extract_first():
                make = d.css("dd.attributeValue-2574930263::text").extract_first()
            elif "Model" == d.css("dt::text").extract_first():
                model = d.css("dd.attributeValue-2574930263::text").extract_first()
            elif "Colour" == d.css("dt::text").extract_first():
                color = d.css("dd.attributeValue-2574930263::text").extract_first()
            elif "Kilometers" in d.css("dt::text").extract_first():
                km = d.css("dd.attributeValue-2574930263::text").extract_first()
            elif "Engine Displacement (cc)" in d.css("dt::text").extract_first():
                engn = d.css("dd.attributeValue-2574930263::text").extract_first()
            elif "Year" in d.css("dt::text").extract_first():
                year = d.css("dd.attributeValue-2574930263::text").extract_first()
            else:
                continue


        yield {
            "Name": name,
            "Model": model,
            "Make": make,
            "Color": color,
            "Kilometers": km,
            "Engine Displacement(cc)": engn,
            "Year": year,
            "URL": response.url,
        }



process = CrawlerProcess()
process.crawl(Playbook)
process.start()
