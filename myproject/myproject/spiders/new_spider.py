import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["finance.yahoo.com"]

    def __init__(self, stock_name=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://finance.yahoo.com/quote/{stock_name}/news/"]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    }

    def parse(self, response):
        position = 1
        while position <= 20:
            title_selector = self.construct_css_selector("title", position)
            description_selector = self.construct_css_selector("description", position)

            title_elements = response.css(title_selector)
            description_elements = response.css(description_selector)

            title_text = title_elements.css("::text").get()
            description_text = description_elements.css("::text").get()

            if title_text and description_text:
                yield {
                    "title": title_text.strip(),
                    "description": description_text.strip(),
                }
            position += 1

    def construct_css_selector(self, selector_type, position):
        base_selectors = {
            "title": "#nimbus-app > section > section > section > article > section.mainContent.yf-1tfxw1f > div > div > div > ul > li:nth-child(POSITION) > section > div > a > h3",
            "description": "#nimbus-app > section > section > section > article > section.mainContent.yf-1tfxw1f > div > div > div > ul > li:nth-child(POSITION) > section > div > a > p",
        }
        return base_selectors[selector_type].replace("POSITION", str(position))
