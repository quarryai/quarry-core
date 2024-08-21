import io
import re

import html5lib
import html2text
import pandas as pd
from lxml import html, etree
from lxml.html import HtmlElement
from bs4 import BeautifulSoup, Tag

from quarry_core.utilities import dataframe_util

newline_placeholder = "[newline]"


class HTML2TextExtended(html2text.HTML2Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Link handling
        self.ignore_links = False  # If True, links will be ignored in the output
        self.inline_links = True
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
        # self.table_content = ""  # Buffer to store table content when bypass_tables is True

        # General formatting
        self.body_width = 0  # Maximum line length for wrapping. 0 means no wrapping.
        self.mark_code = True  # If True, code will be wrapper with [code] block

    def handle_table(self, tag_table: Tag):
        """
        Custom method to handle tables.
        """
        table_html = str(tag_table)

        # Check if the table is inside a code block or part of a link text
        if self.is_in_code_block(tag_table) or self.is_in_link(tag_table):
            return table_html

        dfs = pd.read_html(io.StringIO(table_html))

        if dfs:
            df_clean = dataframe_util.cleanup_html_table_df(df=dfs[0])
            df_markdown = df_clean.to_markdown(index=False)
            df_markdown = df_markdown.replace('\n', newline_placeholder)
        else:
            df_markdown = pd.DataFrame().to_markdown(index=False)

        return f"\n{df_markdown}\n"

    def is_in_code_block(self, soup_element):
        """Check if the element is inside a code block."""
        return soup_element.find_parent('code') is not None

    def is_in_link(self, soup_element):
        """Check if the element is part of a link text."""
        return soup_element.find_parent('a') is not None

    def to_plaintext(self, html_tree: HtmlElement):
        return self.handle(html.tostring(html_tree).decode("utf-8"))

    def to_markdown(self, html_tree: HtmlElement):
        """
        Override the handle method to implement our custom table handling with newline preservation.
        """
        soup = BeautifulSoup(html.tostring(html_tree).decode("utf-8"), "lxml")

        # Find all tables and replace them with our custom handling
        for table in soup.find_all('table'):
            converted_table = self.handle_table(table)
            # Replace newlines with the placeholder
            new_element = BeautifulSoup(converted_table, "lxml")
            table.replace_with(new_element)

        # Convert the modified HTML to markdown using the parent class method
        markdown_content = super().handle(str(soup))

        # Replace the placeholders with actual newlines
        return (
            markdown_content.replace(newline_placeholder, '\n')
            .replace("[code]", "\n```\n")
            .replace("[/code]", "\n```\n")
            .replace("[NBSP]", " ")
        )
