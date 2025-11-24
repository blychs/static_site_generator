import unittest
from generate_html import extract_title


class TestGenerateHTML(unittest.TestCase):
    def test_extract_titles_only_one(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual("Hello", title)

    def test_extract_title_wrong(self):
        md = """## lala
lele
#### lili"""
        with self.assertRaises(Exception):
            extract_title(md)


    def test_extract_title_middle(self):
        md = """
        ## lele
        # li
        No soy
        """
        title = extract_title(md)
        self.assertEqual("li", title)
