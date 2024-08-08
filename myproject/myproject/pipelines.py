import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["finance.yahoo.com"]

    def __init__(self, url='', title='', description='', *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.title_selector = title
        self.description_selector = description

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        if response.status == 404:
            self.log("Page not found (404): {}".format(response.url))
            return

        for position in range(1, 21):  # Iterate through positions 1 to 20
            title_css = self.construct_css_selector(self.title_selector, position)
            description_css = self.construct_css_selector(self.description_selector, position)

            element_title = response.css(title_css).get()
            element_desc = response.css(description_css).get()

            if element_title and element_desc:
                yield {
                    'title': element_title.strip(),
                    'description': element_desc.strip()
                }
            else:
                self.log("No data found at position {} for URL: {}".format(position, response.url))

    def construct_css_selector(self, base_selector, position):
        """
        Constructs a CSS selector from a base pattern and position.

        Parameters:
        - base_selector (str): The base pattern of the CSS selector.
        - position (int): The position of the item to select (1-based index).

        Returns:
        - str: The constructed CSS selector.
        """
        return base_selector.replace('POSITION', f'nth-child({position})')
