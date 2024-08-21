import asyncio
from typing import Dict, List, Any
from lxml import html
from lxml.html import HtmlElement
from quarry_core.framework.data.formatter.html.html_to_dict_transformer import HTMLTransformer
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
    metadata: Dict = HTMLMetadataExtractor(tree=orig_tree).try_get_all()

    # Clean up the HTML tree
    sanitizer: LxmlHTMLTreeSanitizer = LxmlHTMLTreeSanitizer(url=downloaded_html.url, tree=orig_tree)

    if sanitizer.cleanup(config=HTMLTreeSanitizerConfig()):
        # Convert sanitized HTML to plaintext as a first step using HTML2Text and then to final HTML tree
        tree_sanitized: HtmlElement = sanitizer.sanitize()

        # JSON
        # dict_unstructured = HTMLTransformer.to_dict_unstructured(tree_sanitized)
        # dict_beautifulsoup = HTMLTransformer.to_dict_beautifulsoup(tree_sanitized)

        # Markdown - Seems to work well with tree cleaned vs sanitized
        markdown: str = HTMLTransformer.to_markdown(sanitizer.tree_cleaned)

        # HTML
        # html_tree: str = HTMLTransformer.to_html_str(tree_sanitized)

        # Extract various elements
        images: List[Dict[str, Any]] = HTMLDataElementsExtractor.try_extract_images(
            tree=tree_sanitized, base_url=downloaded_html.url
        )
        links: List[Dict[str, Any]] = HTMLDataElementsExtractor.try_extract_links(tree=tree_sanitized)
        tables = HTMLDataElementsExtractor.try_extract_tables(tree=tree_sanitized)

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
