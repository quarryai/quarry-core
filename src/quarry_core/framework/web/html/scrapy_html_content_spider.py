from typing import Any, Callable, Dict, List
import scrapy
from scrapy.http import HtmlResponse


class ScrapyHTMLContentSpider(scrapy.Spider):
    """
    A Scrapy spider for fetching HTML content from a given URL.

    This spider is designed to scrape a single URL and return the HTML content
    along with the URL itself. It uses a callback function to process the
    scraped data.
    """

    name: str = "ScrapyHTMLContentSpider"

    def __init__(
        self, url: str, callback: Callable[[Dict[str, Any]], None], *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize the ScrapyHTMLContentSpider.

        Args:
            url (str): The URL to scrape.
            callback (Callable[[Dict[str, Any]], None]): A function to call with the scraped data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(ScrapyHTMLContentSpider, self).__init__(*args, **kwargs)
        self.start_urls: List[str] = [url]
        self.callback: Callable[[Dict[str, Any]], None] = callback

    def parse(self, response: HtmlResponse, **kwargs: Any) -> None:
        """
        Parse the response and extract the required data.

        This method is called for each response generated for the spider.
        It creates a dictionary with the URL and HTML content, then calls
        the callback function with this data.

        Args:
            response (HtmlResponse): The response object from the HTTP request.
            **kwargs: Arbitrary keyword arguments.
        """
        item: Dict[str, Any] = {
            "url": response.url,
            "content": response.body,
        }
        self.callback(item)
