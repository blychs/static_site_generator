import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_default_build(self):
        node = HTMLNode()
        represent = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(repr(node), represent)

    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        html_props = node.props_to_html()
        self.assertEqual(html_props, 'href="https://www.google.com" target="_blank"')

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

    def test_constructor(self):
        node = LeafNode("a", "lalala")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "lalala")

    def test_constructor_with_props(self):
        node = LeafNode(
            tag=None,
            value="wanabe",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        leaf_props = node.props_to_html()
        self.assertEqual(leaf_props, 'href="https://www.google.com" target="_blank"')

    def test_to_html_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        text = "This is a test"
        node = LeafNode(None, text)
        self.assertEqual(node.to_html(), text)

    def test_to_html(self):
        text = "This is a test"
        tag = "div"
        node = LeafNode(tag, text)
        self.assertEqual(node.to_html(), f"<{tag}>{text}</{tag}>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_default_build(self):
        node = LeafNode("p", "This is a paragraph")
        represent = "LeafNode(tag=p, value=This is a paragraph, props=None)"
        self.assertEqual(repr(node), represent)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrandchildren(self):
        greatgrandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode("p", [greatgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandchild</b></p></span></div>",
        )

    def test_to_html_parent_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_to_html_parent_no_tags(self):
        with self.assertRaises(ValueError):
            child = LeafNode("b", "child")
            node = ParentNode(None, [child])
            node.to_html()

    def test_to_html_parent_no_tags_nolist(self):
        with self.assertRaises(ValueError):
            child = LeafNode("b", "child")
            node = ParentNode(None, child)
            node.to_html()
