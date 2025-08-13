import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_build(self):
        node = HTMLNode()
        represent = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(repr(node), represent)

    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        html_props = node.props_to_html()
        self.assertEqual(html_props,  'href="https://www.google.com" target="_blank"')

    def test_props_empty(self):
        node = HTMLNode()
        html_props = node.props_to_html()
        self.assertEqual(html_props, None)

    def test_only_one_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        html_props = node.props_to_html()
        self.assertEqual(html_props, 'href="https://www.google.com"')

    def test_empty_props_dict(self):
        node = HTMLNode(props={})
        html_props = node.props_to_html()
        self.assertEqual(html_props, "")

    def test_tag(self):
        node = HTMLNode("div", "I am tired")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I am tired")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
