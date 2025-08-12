import unittest
from enum import Enum

from textnode import TextNode, TextType


class TestTextType(unittest.TestCase):
    def test_enum(self):
        self.assertTrue(issubclass(TextType, Enum))


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url2(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.hotmail.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_textType(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_wrong_texttype(self):
        with self.assertRaises(AttributeError):
            TextNode("This is a text node", TextType.ITALIc)

    def test_repr_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_string = "TextNode(This is a text node, TextType.BOLD, None)"
        self.assertEqual(repr(node), expected_string)

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        expected_string = "TextNode(This is a text node, TextType.LINK, www.google.com)"
        self.assertEqual(repr(node), expected_string)


if __name__ == "__main__":
    unittest.main()
