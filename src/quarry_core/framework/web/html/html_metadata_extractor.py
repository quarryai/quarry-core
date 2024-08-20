from typing import List, Optional
from datetime import datetime
from lxml.html import HtmlElement

from quarry_core.framework.web.html.html_element_xpaths import HTMLElementXPaths
from quarry_core.utilities import datetime_util
from quarry_core.utilities.constants import AUTHOR_PREFIXES


class HTMLMetadataExtractor:
    """A class for extracting and storing metadata from HTML documents."""

    @staticmethod
    def try_extract_title(tree: HtmlElement) -> Optional[str]:
        """Extract the title from the HTML tree."""
        title: Optional[str] = None

        for xpath in HTMLElementXPaths.TITLE:
            titles = tree.xpath(xpath)
            if titles:
                title = titles[0].strip()

        return title

    @staticmethod
    def try_extract_description(tree: HtmlElement) -> Optional[str]:
        """Extract the description from the HTML tree."""
        description: Optional[str] = None

        for xpath in HTMLElementXPaths.DESCRIPTION:
            descriptions = tree.xpath(xpath)

            if descriptions:
                description = descriptions[0].strip()

        return description

    @staticmethod
    def try_extract_keywords(tree: HtmlElement) -> Optional[List[str]]:
        """Extract the keywords from the HTML tree."""
        keywords: Optional[List[str]] = None

        for xpath in HTMLElementXPaths.KEYWORDS:
            keywords = tree.xpath(xpath)

            if keywords:
                keywords = [kw.strip() for kw in keywords]

        return keywords

    @staticmethod
    def try_extract_publish_time(tree: HtmlElement) -> Optional[datetime]:
        """Extract and parse the publication time from the HTML tree."""

        published_time: Optional[datetime] = None

        for xpath in HTMLElementXPaths.PUBLISHED_TIME:
            published_times = tree.xpath(xpath)

            if published_times:
                published_time = datetime_util.try_parse_datetime(published_times[0])

        return published_time

    @staticmethod
    def try_extract_authors(tree: HtmlElement) -> Optional[List[str]]:
        """Extract and clean author names from the HTML tree."""
        authors: List[str] = []

        for xpath in HTMLElementXPaths.AUTHOR:
            authors = tree.xpath(xpath)

            for author in authors:
                cleaned_author = HTMLMetadataExtractor._clean_author_name(author)
                if cleaned_author and cleaned_author not in authors:
                    authors.append(cleaned_author)

        return authors if authors else None

    @staticmethod
    def _clean_author_name(author: str) -> str:
        """
        Clean an author name by removing common prefixes and extra whitespace.
        """
        for prefix in AUTHOR_PREFIXES:
            if author.startswith(prefix):
                author = author[len(prefix) :]
                break

        return " ".join(author.split()).strip()
