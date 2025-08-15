from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode 


def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    text = text_node.text
    props = None
    match text_type:
        case TextType.TEXT:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            props = {'href': text_node.url}
            return LeafNode("a", text, props)
        case TextType.IMAGE:
            props = {'src': text_node.url, 'alt': text_node.text}
            return LeafNode("img", "", props)
        case _:
            raise ValueError(f"{text_node.text_type} is not in TextType")
