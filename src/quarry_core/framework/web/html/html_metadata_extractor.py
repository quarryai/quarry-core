from typing import List, Optional
from datetime import datetime
from lxml.html import HtmlElement

from quarry_core.framework.web.html.html_element_xpaths import HTMLElementXPaths
from quarry_core.utilities import datetime_util
from quarry_core.utilities.constants import AUTHOR_PREFIXES


class HTMLMetadataExtractor:
    """A class for extracting and storing metadata from HTML documents."""

    def __init__(self, tree: HtmlElement):
        self._tree = tree

    def try_get_all(self):
        """Extract all metadata from the HTML tree."""
        return {
            "title": self.try_get_title(),
            "description": self.try_get_description(),
            "authors": self.try_get_authors(),
            "published_time": self.try_get_publish_time(),
            "keywords": self.try_get_keywords(),
        }

    def try_get_title(self) -> Optional[str]:
        """Extract the title from the HTML tree."""
        title: Optional[str] = None

        for xpath in HTMLElementXPaths.TITLE:
            titles = self._tree.xpath(xpath)
            if titles:
                title = titles[0].strip()

        return title

    def try_get_description(self) -> Optional[str]:
        """Extract the description from the HTML tree."""
        description: Optional[str] = None

        for xpath in HTMLElementXPaths.DESCRIPTION:
            descriptions = self._tree.xpath(xpath)

            if descriptions:
                description = descriptions[0].strip()
                break

        return description

    def try_get_keywords(self) -> Optional[List[str]]:
        """Extract the keywords from the HTML tree."""
        keywords: Optional[List[str]] = []

        for xpath in HTMLElementXPaths.KEYWORDS:
            extracted_keywords = self._tree.xpath(xpath)

            if extracted_keywords:
                for kws in extracted_keywords:
                    keywords.extend([kw.strip() for kw in kws.split(",")])

        return keywords

    def try_get_publish_time(self) -> Optional[datetime]:
        """Extract and parse the publication time from the HTML tree."""

        published_time: Optional[datetime] = None

        for xpath in HTMLElementXPaths.PUBLISHED_TIME:
            published_times = self._tree.xpath(xpath)

            if published_times:
                published_time = datetime_util.try_parse_datetime(published_times[0])

        return published_time

    def try_get_authors(self) -> Optional[List[str]]:
        """Extract and clean author names from the HTML tree."""
        authors: List[str] = []

        for xpath in HTMLElementXPaths.AUTHOR:
            extracted_authors = self._tree.xpath(xpath)

            for author in extracted_authors:
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
                author = author[len(prefix):]
                break

        return " ".join(author.split()).strip()
