import io
import re

import markdown2
import pandas as pd

from lxml import html
from lxml.html import HtmlElement

from quarry_core.libs.framework.utils.data.helpers import dataframe_util


class MarkdownTransformer:
    """A class for processing and converting markdown content to various formats."""

    @staticmethod
    def to_html_lxml(plaintext: str, replace_code_block: bool = True) -> HtmlElement:
        """
        Convert plaintext with custom code tags to HTML.

        Args:
            plaintext (str): The input Markdown text.
            replace_code_block (bool): Handle replacement of code blocks [code][/code].
        Returns:
            str: The converted HTML.
        """

        preprocessed = plaintext.replace("[code]", "<pre><code>").replace("[/code]", "</code></pre>")
        return html.fromstring(f"<html>\n<body>\n{markdown2.markdown(preprocessed)}\n</body>\n</html>")

    @staticmethod
    def html_table_to_pipe(html_table):
        rows = re.findall(r'<tr>(.*?)</tr>', html_table, re.DOTALL)
        pipe_rows = []
        for row in rows:
            cells = re.findall(r'<t[hd]>(.*?)</t[hd]>', row, re.DOTALL)
            pipe_cells = [cell.strip().replace('\n', ' ') for cell in cells]
            pipe_rows.append('| ' + ' | '.join(pipe_cells) + ' |')

        if len(pipe_rows) > 1:
            pipe_rows.insert(1, '| ' + ' | '.join(['---'] * len(cells)) + ' |')

        return '\n'.join(pipe_rows)

    @staticmethod
    def replace_tables(markdown):
        def replace_table(match):
            html_table = match.group(0)
            return MarkdownTransformer.html_table_to_pipe(html_table)

        # Pattern to match standalone HTML tables
        table_pattern = r'<table>(?:\s*<tr>.*?</tr>)+\s*</table>'

        # Replace tables outside of code blocks
        parts = re.split(r'(\[code\].*?\[/code\])', markdown, flags=re.DOTALL)
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(table_pattern, replace_table, parts[i], flags=re.DOTALL)

        return ''.join(parts)

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
        in_link_block = False

        for line in lines:
            if "[code]" in line:
                in_code_block = True
                processed_lines.append(line)
            if "[/code]" in line:
                in_code_block = False
                processed_lines.append(line)
            if "**[" in line:
                in_link_block = True
                processed_lines.append(line)
            if ")**" in line:
                in_link_block = False
                processed_lines.append(line)
            if not in_code_block and not in_link_block and "<table>" in line:
                in_table = True
                table_lines = [line]
            if in_table and "</table>" in line:
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

            if in_table and not in_code_block and not in_link_block:
                table_lines.append(line)
            else:
                processed_lines.append(line)

        mkdwn = "\n".join(processed_lines)

        if replace_code_block:
            mkdwn = mkdwn.replace("[code]", "```\n").replace("[/code]", "```\n")

        return mkdwn
