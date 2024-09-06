import os
from typing import List, Dict, Any
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from quarry_core.libs.framework.utils.web.scrapy_html_content_spider import ScrapyHTMLContentSpider
from quarry_core.libs.framework.utils.web.html_page_content import HTMLPageContent


class ScrapyHTMLLoader:
    """
    A loader class for fetching HTML content using Scrapy.

    Attributes:
        results (List[HTMLPageContent]): A list to store the results of the spider.
        settings (Settings): Scrapy settings for the crawler.
    """

    def __init__(self) -> None:
        """
        Initialize the ScrapyHTMLLoader.
        """
        self.results: List[HTMLPageContent] = []
        self.settings: Settings = self._get_scrapy_settings()

    def _get_scrapy_settings(self) -> Settings:
        """
        Get and configure Scrapy settings.

        Returns:
            Settings: Configured Scrapy settings.
        """
        settings = get_project_settings()
        settings.set("ROBOTSTXT_OBEY", False)
        settings.set("LOG_LEVEL", "WARNING")
        settings.set("DOWNLOAD_DELAY", float(os.getenv("DOWNLOAD_DELAY", "1")))
        settings.set("CONCURRENT_REQUESTS_PER_DOMAIN", int(os.getenv("CONCURRENT_REQUESTS", "2")))
        settings.set(
            "DOWNLOADER_MIDDLEWARES",
            {
                "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None
            },
        )
        settings.set("EXTENSIONS", {"scrapy.extensions.telnet.TelnetConsole": None})
        settings.set("REQUEST_FINGERPRINTER_IMPLEMENTATION", "2.7")

        return settings

    def fetch(self, url: str) -> HTMLPageContent:
        """
        Fetch HTML content from a given URL using Scrapy.

        Args:
            url (str): The URL to fetch content from.

        Returns:
            Tuple[bytes, str]: A tuple containing the content (as bytes) and the URL.
        """
        self.results = []

        process: CrawlerProcess = CrawlerProcess(self.settings)
        process.crawl(ScrapyHTMLContentSpider, url=url, callback=self._store_result)
        process.start()

        if self.results:
            return self.results[0]
        else:
            return HTMLPageContent(html=b"", url=url)

    def _store_result(self, item: Dict[str, Any]) -> None:
        """
        Store the result of the spider in the results list.

        Args:
            item (Dict[str, Any]): A dictionary containing the scraped content and URL.
        """
        self.results.append(HTMLPageContent(url=item.get("url"), html=item.get("content", b"")))
