import asyncio
from typing import Dict, List, Any, Optional
from lxml import html
from lxml.html import HtmlElement
from quarry_core.framework.data.formatter.html.html_to_dict_formatter import HTMLToDictFormatter
from quarry_core.framework.data.formatter.markdown.markdown_formatter import MarkdownFormatter
from quarry_core.framework.web.html.html2text_extended import HTML2TextExtended
from quarry_core.framework.web.html.html_data_elements_extractor import HTMLDataElementsExtractor
from quarry_core.framework.web.html.html_metadata_extractor import HTMLMetadataExtractor
from quarry_core.framework.web.html.html_page_content import HTMLPageContent
from quarry_core.framework.web.html.html_tree_sanitizer_config import HTMLTreeSanitizerConfig
from quarry_core.framework.web.html.lxml_html_tree_sanitizer import LxmlHTMLTreeSanitizer
from quarry_core.framework.web.html.scrapy_html_loader import ScrapyHTMLLoader


# Test links for scraping

TEST_LINKS: Dict[str, str] = {
    "tables": "https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables/Basics",
    "coindesk": "https://www.coindesk.com/markets/2024/08/16/record-drop-in-ethereum-gas-fees-marks-historically-bullish-signal-for-eth-analyst-says/",
}


async def main() -> None:
    # Fetch the HTML content
    downloaded_html: HTMLPageContent = ScrapyHTMLLoader().fetch(TEST_LINKS["tables"])

    # Parse the HTML into a tree structure
    orig_tree: HtmlElement = html.fromstring(downloaded_html.html)

    # Extract metadata
    title: Optional[str] = HTMLMetadataExtractor.try_extract_title(tree=orig_tree)
    description: Optional[str] = HTMLMetadataExtractor.try_extract_description(tree=orig_tree)
    keywords: Optional[List[str]] = HTMLMetadataExtractor.try_extract_keywords(tree=orig_tree)
    authors: Optional[List[str]] = HTMLMetadataExtractor.try_extract_authors(tree=orig_tree)
    published_time: Optional[str] = HTMLMetadataExtractor.try_extract_publish_time(tree=orig_tree)

    # Clean up the HTML tree
    sanitized_tree: Optional[HtmlElement] = (
        LxmlHTMLTreeSanitizer(url=downloaded_html.url, tree=orig_tree)
        .sanitize(config=HTMLTreeSanitizerConfig())
        .set_urls_to_abs()
        .try_get_body()
    )

    if sanitized_tree is not None:
        # Convert sanitized HTML to plaintext as a first step using HTML2Text and then to final HTML tree
        plaintext: str = HTML2TextExtended().to_plaintext(sanitized_tree)
        final_tree: HtmlElement = MarkdownFormatter.to_html_lxml(plaintext)

        # Extract various elements
        images: List[Dict[str, Any]] = HTMLDataElementsExtractor.try_extract_images(
            tree=final_tree, base_url=downloaded_html.url
        )
        links: List[Dict[str, Any]] = HTMLDataElementsExtractor.try_extract_links(tree=final_tree)
        tables = HTMLDataElementsExtractor.try_extract_tables(tree=final_tree)

        # Parse content into different formats:

        # JSON
        dict_unstructured = HTMLToDictFormatter.to_dict_unstructured(final_tree)
        dict_beautifulsoup = HTMLToDictFormatter.to_dict_beautifulsoup(final_tree)
        # Markdown
        markdown = HTML2TextExtended().to_plaintext(final_tree)

        pass

        # Construct and return the result dictionary
        # doc = {
        #     "url": downloaded_html.url,
        #     "title": title,
        #     "authors": authors,
        #     "published_time": published_time,
        #     "document": parsed_markdown,
        #     "type": "markdown",
        #     "elements": {
        #         "links": links,
        #         "tables": tables,
        #         "images": images,
        #         "codeblocks": []
        #     },
        #     "tags": tags,
        # }


if __name__ == "__main__":
    asyncio.run(main())
