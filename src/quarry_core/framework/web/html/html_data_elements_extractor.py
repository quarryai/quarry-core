from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from lxml import etree
from lxml.html import HtmlElement

from quarry_core.utilities import dataframe_util


class HTMLDataElementsExtractor:
    """A utility class for extracting various elements from HTML content."""

    @staticmethod
    def try_extract_links(tree: HtmlElement) -> List[Dict[str, Any]]:
        """
        Extract links from the HTML content tree.

        Args:
            tree (HtmlElement): The HTML content tree to extract links from.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing link information.
                Each dictionary has 'title' and 'url' keys.
        """
        links: List[Dict[str, Any]] = []

        for index, a in enumerate(tree.xpath("//a[@href]")):
            href: Optional[str] = a.get("href")

            if href and urlparse(href).scheme and urlparse(href).netloc:
                text: str = a.text_content().strip()
                links.append({"title": text if text else f"unnamed_{index}", "url": href})

        return links

    @staticmethod
    def try_extract_images(tree: HtmlElement, base_url: str) -> List[Dict[str, Any]]:
        """
        Extract image information from the HTML content tree.

        Args:
            tree (HtmlElement): The HTML content tree to extract images from.
            base_url (str): The base URL to use for resolving relative image URLs.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing image information.
                Each dictionary includes 'index', 'url', and other available attributes.
        """
        images: List[Dict[str, Any]] = []
        for index, img in enumerate(tree.xpath("//img[@src]")):
            src: Optional[str] = img.get("src")
            if src:
                image_info: Dict[str, Any] = {
                    "index": index,
                    "url": urljoin(base_url, src),
                }
                for attr in ["alt", "title", "width", "height", "class", "id", "loading", "srcset"]:
                    if value := img.get(attr):
                        image_info[attr] = value
                images.append(image_info)
        return images

    @staticmethod
    def try_extract_tables(tree: HtmlElement) -> List[List[Dict[str, Any]]]:
        """
        Extract tables from an HtmlElement and convert them to a list of list of dictionaries.

        Args:
            tree (HtmlElement): The HtmlElement containing tables.

        Returns:
            List[List[Dict[str, Any]]]: A list of tables, where each table is a list of dictionaries.
                Each dictionary represents a row in the table.

        Raises:
            ValueError: If no tables are found in the HTML content.
        """
        # Convert HtmlElement to string
        # Convert HtmlElement to string, preserving HTML structure
        html_str = etree.tostring(tree, encoding='unicode', method='html')

        # Parse the HTML using Beautiful Soup
        soup = BeautifulSoup(html_str, 'lxml')

        # Find all table elements
        tables = soup.find_all('table')

        if not tables:
            return []

        return [dataframe_util.cleanup_html_table_df(df=df).to_dict("records") for df in tables]
