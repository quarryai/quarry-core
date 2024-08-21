import io

import html2text
import pandas as pd
from lxml import etree
from lxml.html import HtmlElement

from quarry_core.utilities import dataframe_util


class HTML2TextLxml(html2text.HTML2Text):

    NEWLINE_PLACEHOLDER: str = "[newline]"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Link handling
        self.ignore_links = False
        self.inline_links = True
        self.wrap_links = False
        self.skip_internal_links = False
        self.links_each_paragraph = True

        # List handling
        self.wrap_lists = False

        # Image handling
        self.ignore_images = False
        self.default_image_alt = "Image"

        # Table handling
        self.ignore_tables = False
        self.bypass_tables = True

        self.in_table = False

        # General formatting
        self.body_width = 0
        self.mark_code = True

    def handle_table(self, table_element):
        """
        Custom method to handle tables.
        """
        table_html = etree.tostring(table_element, encoding='unicode')

        # Check if the table is inside a code block or part of a link text
        if self.is_embedded_table(table_element):
            return table_html

        dfs = pd.read_html(io.StringIO(table_html))

        if dfs:
            df_clean = dataframe_util.cleanup_html_table_df(df=dfs[0])
            df_markdown = df_clean.to_markdown(index=False)
            # IMPORTANT: To preserve the markdown pipe formatting for the table
            df_markdown = df_markdown.replace("\n", self.NEWLINE_PLACEHOLDER)
        else:
            df_markdown = pd.DataFrame().to_markdown(index=False)

        return f"\n{df_markdown}\n"

    def is_embedded_table(self, element):
        """Check if the element is directly inside a code block or a link."""
        parent = element.getparent()
        return parent is not None and parent.tag in ["code", "a"]

    def to_plaintext(self, html_tree: HtmlElement):
        return self.handle(etree.tostring(html_tree, encoding='unicode'))

    def to_markdown(self, html_tree: HtmlElement):
        """
        Override the handle method to implement our custom table handling with newline preservation.
        """
        # Create a new tree to modify
        parser = etree.HTMLParser()
        tree = etree.parse(io.StringIO(etree.tostring(html_tree, encoding='unicode')), parser)
        root = tree.getroot()

        # Find all tables and replace them with our custom handling
        for table in root.xpath('//table'):
            converted_table = self.handle_table(table)
            new_element = etree.fromstring(f'<div>{converted_table}</div>')
            table.getparent().replace(table, new_element)

        # Convert the modified HTML to markdown using the parent class method
        markdown_content = super().handle(etree.tostring(root, encoding='unicode'))

        # Replace the placeholders with actual newlines
        return (
            markdown_content.replace(self.NEWLINE_PLACEHOLDER, "\n")
            .replace("[code]", "\n```\n")
            .replace("[/code]", "\n```\n")
            .replace("[NBSP]", " ")
        )
