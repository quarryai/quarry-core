from urllib.parse import urljoin
from typing import Optional, List
from lxml.html import HtmlElement

from quarry_core.framework.web.html.html_element_xpaths import HTMLElementXPaths
from quarry_core.framework.web.html.html_tree_sanitizer_config import HTMLTreeSanitizerConfig


class LxmlHTMLTreeSanitizer:
    """
    A class for sanitizing and processing HTML content using lxml.

    This class provides methods to remove unwanted elements from an HTML tree,
    extract main content, and convert relative URLs to absolute URLs.
    """

    _tree_cleaned: Optional[HtmlElement] = None

    def __init__(self, url: str, tree: HtmlElement):
        self.tree: HtmlElement = tree
        self.url = url

    def cleanup(self, config: Optional[HTMLTreeSanitizerConfig] = None) -> 'LxmlHTMLTreeSanitizer':
        """
        Cleanup the HTML tree by removing unwanted elements based on the provided configuration.

        Args:
            config (Optional[HTMLTreeSanitizerConfig]): The sanitization configuration. If None, default config is used.

        Returns:
            LxmlHTMLTreeSanitizer: The current instance for method chaining.
        """
        if config is None:
            config = HTMLTreeSanitizerConfig()

        body: List[HtmlElement] = self.tree.xpath("//body")

        if not body:
            self._tree_cleaned = None
        else:
            self._tree_cleaned = body[0]
            excluded_elements: List[str] = self._get_excluded_elements(config)
            self._remove_elements(self._tree_cleaned, excluded_elements)

        return self

    def try_get_body(self) -> Optional[HtmlElement]:
        """
        Attempt to get the sanitized body of the HTML.

        Returns:
            Optional[HtmlElement]: The sanitized body if available, None otherwise.
        """
        return self._tree_cleaned

    def try_get_article(self) -> Optional[HtmlElement]:
        """
        Attempt to extract the main article from the sanitized HTML body.

        Returns:
            Optional[HtmlElement]: The main content element if found, None otherwise.
        """
        if self._tree_cleaned is None:
            return None

        for xpath in HTMLElementXPaths.ARTICLE:
            main_content: List[HtmlElement] = self._tree_cleaned.xpath(xpath)
            if main_content:
                return main_content[0]

        return None

    def set_urls_to_abs(self) -> 'LxmlHTMLTreeSanitizer':
        """
        Convert relative URLs to absolute URLs in the sanitized HTML body.

        Returns:
            LxmlHTMLTreeSanitizer: The current instance for method chaining.
        """
        if self._tree_cleaned is None:
            return self

        for element in self._tree_cleaned.xpath(".//*[@src or @href]"):
            for attr in ["src", "href"]:
                if element.get(attr):
                    element.set(attr, urljoin(self.url, element.get(attr)))

        return self

    def _get_excluded_elements(self, config: HTMLTreeSanitizerConfig) -> List[str]:
        """
        Generate a list of XPath expressions for elements to be excluded based on the configuration.

        Args:
            config (HTMLTreeSanitizerConfig): The sanitization configuration.

        Returns:
            List[str]: A list of XPath expressions for elements to be excluded.
        """
        excluded_elements: List[str] = []

        if not config.include_header:
            excluded_elements.extend(HTMLElementXPaths.HEADER)
        if not config.include_footer:
            excluded_elements.extend(HTMLElementXPaths.FOOTER)
        if not config.include_nav:
            excluded_elements.extend(HTMLElementXPaths.NAV)
        if not config.include_comments:
            excluded_elements.extend(HTMLElementXPaths.COMMENTS)
        if not config.include_social:
            excluded_elements.extend(HTMLElementXPaths.SOCIAL)
        if not config.include_ads:
            excluded_elements.extend(HTMLElementXPaths.ADS)
        if not config.include_misc:
            excluded_elements.extend(HTMLElementXPaths.MISC)

        return excluded_elements

    @staticmethod
    def _remove_elements(tree: HtmlElement, xpath_list: List[str]) -> None:
        """
        Remove elements from the HTML tree based on a list of XPath expressions.

        Args:
            tree (HtmlElement): The HTML tree to modify.
            xpath_list (List[str]): A list of XPath expressions for elements to remove.
        """
        for xpath in xpath_list:
            elements: List[HtmlElement] = tree.xpath(xpath)
            for element in elements:
                parent: Optional[HtmlElement] = element.getparent()
                if parent is not None:
                    parent.remove(element)
