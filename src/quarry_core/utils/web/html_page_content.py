from pydantic import BaseModel


class HTMLPageContent(BaseModel):
    """
    Pydantic model for storing the result of a Scrapy spider.

    Attributes:
        url (str): The URL of the scraped page.
        html (bytes): The html content of the scraped page.
    """

    url: str
    html: bytes
