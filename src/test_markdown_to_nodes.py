import unittest

from markdown_to_nodes import markdown_to_html_node


class TestMarkdownToNodes(unittest.TestCase):
    """Unit tests for the markdown_to_nodes function."""

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_quote_to_html(self):
        md = """
>This is a blockquote with **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <b>bold</b> text</blockquote></div>",
        )


    def test_multiline_quote_to_html(self):
        md = """
>This is a blockquote
>with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <b>bold</b> text</blockquote></div>",
            )


    def test_unordered_list(self):
        md = """
- I'm testing this
- Maybe it works
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><ul><li>I'm testing this</li><li>Maybe it works</li></ul></div>"
                )


    def test_unordered_list_mixed(self):
        md = """
- But I'll have some `code`
- And also some **bold** and _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><ul><li>But I'll have some <code>code</code></li><li>And also some <b>bold</b> and <i>italic</i> text</li></ul></div>"
                )


    def test_ordered_list(self):
        md = """
1. I'm testing this
2. Maybe it works
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><ol><li>I'm testing this</li><li>Maybe it works</li></ol></div>"
                )


    def test_ordered_list_mixed(self):
        md = """
1. But I'll have some `code`
2. And also some **bold** and _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><ol><li>But I'll have some <code>code</code></li><li>And also some <b>bold</b> and <i>italic</i> text</li></ol></div>"
                )
