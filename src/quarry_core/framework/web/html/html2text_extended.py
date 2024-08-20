import html2text
from lxml import html
from lxml.html import HtmlElement


class HTML2TextExtended(html2text.HTML2Text):
    """
    An extended version of the HTML2Text class with additional configuration options.

    This class provides more granular control over the HTML to Markdown conversion process,
    allowing for customization of link handling, list formatting, image processing, and more.
    """

    def __init__(self, **kwargs):
        """
        Initialize the ExtendedHTML2Text instance with custom configurations.
        """
        super().__init__(**kwargs)

        # Link handling
        self.ignore_links = False  # If True, links will be ignored in the output
        self.wrap_links = False  # If True, links will be wrapped to the next line
        self.skip_internal_links = False  # If True, internal links (starting with #) will be skipped
        self.links_each_paragraph = True  # If True, links are placed after each paragraph

        # List handling
        self.wrap_lists = False  # If True, list items will be wrapped to the next line

        # Image handling
        self.ignore_images = False  # If True, images will be ignored in the output
        self.default_image_alt = "Image"  # Default alt text for images if not provided

        # Table handling
        self.ignore_tables = False  # If True, tables will be completely ignored
        self.bypass_tables = True  # If True, tables will be in HTML format vs converted to Markdown

        self.in_table = False  # Internal flag to track if we're currently processing a table
        self.table_content = ""  # Buffer to store table content when bypass_tables is True

        # General formatting
        self.body_width = 0  # Maximum line length for wrapping. 0 means no wrapping.
        self.mark_code = True  # If True, inline code will be marked with backticks

    def to_plaintext(self, html_tree: HtmlElement):
        return self.handle(html.tostring(html_tree).decode("utf-8"))
