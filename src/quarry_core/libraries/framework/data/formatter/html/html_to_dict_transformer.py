from typing import Union, Dict, Any, List
from bs4 import BeautifulSoup, Tag, NavigableString
from lxml import etree
from lxml.html import HtmlElement
from unstructured.partition.html import partition_html
import nltk

from quarry_core.libraries.framework.web.html_2_text_lxml import HTML2TextLxml

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class HTMLTransformer:
    """
    A class for converting HTML to dictionary representations using different methods.
    """

    def __init__(self):
        pass

    @staticmethod
    def to_html_str(html: HtmlElement) -> str:
        return etree.tostring(html, pretty_print=True, with_tail=False, encoding="Unicode")

    @staticmethod
    def to_plaintext(html: HtmlElement) -> str:
        return HTML2TextLxml().to_plaintext(html_tree=html)

    @staticmethod
    def to_markdown(html: HtmlElement) -> str:
        return HTML2TextLxml().to_markdown(html_tree=html)

    @staticmethod
    def to_dict_unstructured(html: HtmlElement) -> Dict[str, List[Dict[str, Any]]]:
        """
        Convert HTML to a dictionary using the Unstructured library.

        Args:
            html (HtmlElement): The input HTML element.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing a list of parsed elements in the Unstructured.io format.
        """
        html_string = etree.tostring(html, encoding="unicode", with_tail=False)
        elements = partition_html(text=html_string)

        result: Dict[str, List[Dict[str, Any]]] = {"elements": []}
        for element in elements:
            element_dict: Dict[str, Any] = {"type": element.category, "text": element.text}
            if hasattr(element, 'metadata'):
                element_dict["metadata"] = element.metadata
            result["elements"].append(element_dict)

        return result

    @staticmethod
    def to_dict_beautifulsoup(html: HtmlElement) -> List[Dict[str, Any]]:
        """
        Convert HTML to a list of dictionaries using BeautifulSoup for parsing.

        Args:
            html (HtmlElement): The input HTML element.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the parsed HTML structure.
        """
        html_string = etree.tostring(html, encoding="unicode", with_tail=False)
        soup = BeautifulSoup(html_string, 'lxml')

        return [
            HTMLTransformer._parse_beautifulsoup_element(child)
            for child in soup.body.children
            if child != "\n"
        ]

    @staticmethod
    def _parse_beautifulsoup_element(element: Union[Tag, NavigableString]) -> Union[str, Dict[str, Any]]:
        """
        Recursively parse a BeautifulSoup element into a structured dictionary representation.

        Args:
            element (Union[Tag, NavigableString]): The BeautifulSoup element to parse.

        Returns:
            Union[str, Dict[str, Any]]: A string if the element is a text node, otherwise a
            dictionary representing the element's structure.
        """
        if isinstance(element, NavigableString):
            return str(element).strip()

        result: Dict[str, Any] = {"type": element.name}

        if element.attrs:
            result["attributes"] = element.attrs

        if element.name == "img":
            result.update({"src": element.get("src", ""), "alt": element.get("alt", "")})
        elif element.name == "a":
            result.update({"href": element.get("href", ""), "text": element.string or ""})
        else:
            content: List[Union[str, Dict[str, Any]]] = [
                HTMLTransformer._parse_beautifulsoup_element(child)
                for child in element.children
                if not isinstance(child, NavigableString) or child.strip()
            ]
            if content:
                result["content"] = content[0] if len(content) == 1 else content

        return result
