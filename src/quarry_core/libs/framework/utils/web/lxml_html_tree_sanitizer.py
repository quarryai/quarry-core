from urllib.parse import urljoin
from typing import Optional, List
from lxml.html import HtmlElement

from quarry_core.libs.framework.utils.data.formatter.html.html_to_dict_transformer import HTMLTransformer
from quarry_core.libs.framework.utils.data.formatter.markdown.markdown_transformer import MarkdownTransformer
from quarry_core.libs.framework.utils.web.html_element_xpaths import HTMLElementXPaths
from quarry_core.libs.framework.utils.web.html_tree_sanitizer_config import HTMLTreeSanitizerConfig


class LxmlHTMLTreeSanitizer:
    """
    A class for sanitizing and processing HTML content using lxml.

    This class provides methods to remove unwanted elements from an HTML tree,
    extract main content, and convert relative URLs to absolute URLs.
    """

    def __init__(self, url: str, tree: HtmlElement):
        self._orig_tree: HtmlElement = tree
        self.tree_cleaned: Optional[HtmlElement] = None
        self.url = url

    def sanitize(self) -> HtmlElement:
        plaintext: str = HTMLTransformer.to_plaintext(self.tree_cleaned)
        return MarkdownTransformer.to_html_lxml(plaintext)

    def cleanup(self, config: Optional[HTMLTreeSanitizerConfig] = None) -> bool:
        """
        Cleanup the HTML tree by removing unwanted elements based on the provided configuration.

        Args:
            config (Optional[HTMLTreeSanitizerConfig]): The sanitization configuration. If None, default config is used.

        Returns:
            LxmlHTMLTreeSanitizer: The current instance for method chaining.
        """
        if config is None:
            config = HTMLTreeSanitizerConfig()

        body: List[HtmlElement] = self._orig_tree.xpath("//body")

        if not body:
            self.tree_cleaned = None
            return False
        else:
            self.tree_cleaned = body[0]
            excluded_elements: List[str] = self._get_excluded_elements(config)
            self._remove_elements(tree=self.tree_cleaned, excluded_xpaths=excluded_elements)
            self._set_urls_to_abs(tree=self.tree_cleaned, url=self.url)
            return True

    def try_get_article(self) -> Optional[HtmlElement]:
        """
        Attempt to extract the main article from the sanitized HTML body.

        Returns:
            Optional[HtmlElement]: The main content element if found, None otherwise.
        """
        if self.tree_cleaned is None:
            return None

        for xpath in HTMLElementXPaths.ARTICLE:
            main_content: List[HtmlElement] = self.tree_cleaned.xpath(xpath)
            if main_content:
                return main_content[0]

        return None

    @staticmethod
    def _set_urls_to_abs(tree: HtmlElement, url: str):
        """
        Convert relative URLs to absolute URLs in the sanitized HTML body.

        Returns:
            LxmlHTMLTreeSanitizer: The current instance for method chaining.
        """
        if tree is not None:
            for element in tree.xpath(".//*[@src or @href]"):
                for attr in ["src", "href"]:
                    if element.get(attr):
                        element.set(attr, urljoin(url, element.get(attr)))

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
    def _remove_elements(tree: HtmlElement, excluded_xpaths: List[str]) -> None:
        """
        Remove elements from the HTML tree based on a list of XPath expressions.

        Args:
            tree (HtmlElement): The HTML tree to modify.
            excluded_xpaths (List[str]): A list of XPath expressions for elements to remove.
        """
        for xpath in excluded_xpaths:
            elements: List[HtmlElement] = tree.xpath(xpath)
            for element in elements:
                parent: Optional[HtmlElement] = element.getparent()
                if parent is not None:
                    parent.remove(element)
