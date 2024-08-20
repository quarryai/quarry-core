import io

import markdown2
import pandas as pd

from lxml import html
from lxml.html import HtmlElement

from quarry_core.utilities import dataframe_util


class MarkdownFormatter:
    """A class for processing and converting markdown content to various formats."""

    @staticmethod
    def to_html_lxml(markdown: str, replace_code_block: bool = True) -> HtmlElement:
        """
        Convert plaintext with custom code tags to HTML.

        Args:
            markdown (str): The input Markdown text.
            replace_code_block (bool): Handle replacement of code blocks [code][/code].
        Returns:
            str: The converted HTML.
        """

        preprocessed = markdown.replace("[code]", "<pre><code>").replace("[/code]", "</code></pre>")
        return html.fromstring(f"<html>\n<body>\n{markdown2.markdown(preprocessed)}\n</body>\n</html>")

    @staticmethod
    def standardize(markdown: str, replace_code_block: bool = True) -> str:
        """
        Converts HTML2Text Markdown with custom formatting to standard markdown.

        Args:
            markdown (str): The input plaintext with custom formatting.
            replace_code_block (bool): Handle replacement of code blocks [code][/code].

        Returns:
            str: The converted standard markdown.
        """
        lines = markdown.split("\n")
        processed_lines = []
        table_lines = []
        in_table = False
        in_code_block = False

        for line in lines:
            if "[code]" in line:
                in_code_block = True
                processed_lines.append(line)
            elif "[/code]" in line:
                in_code_block = False
                processed_lines.append(line)
            elif not in_code_block and "<table>" in line:
                in_table = True
                table_lines = ["", line]
            elif not in_code_block and "</table>" in line:
                table_lines.append(line)
                table_html = "\n".join(table_lines)
                dfs = pd.read_html(io.StringIO(table_html))
                if dfs:
                    df = dataframe_util.cleanup_html_table_df(dfs[0])
                    processed_tbl = df.to_markdown(index=False)
                    processed_lines.append(processed_tbl)
                else:
                    processed_lines.extend(table_lines)
                in_table = False
                table_lines = []
            elif in_table and not in_code_block:
                table_lines.append(line)
            else:
                processed_lines.append(line)

        mkdwn = "\n".join(processed_lines)

        if replace_code_block:
            mkdwn = mkdwn.replace("[code]", "```\n").replace("[/code]", "```\n")

        return mkdwn
