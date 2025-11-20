import re

from htmlnode import LeafNode  # , HTMLNode, ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    text = text_node.text
    props = None
    if TextType != TextType.CODE:
        text = text.replace("\n", " ")
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
            props = {"href": text_node.url}
            return LeafNode("a", text, props)
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("img", "", props)
        case _:
            raise ValueError(f"{text_node.text_type} is not in TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        url = old_node.url
        nodes_text = old_node.text.split(delimiter)
        if len(nodes_text) % 2 == 0:
            raise ValueError("Not valid markdown, odd number of delimiters")
        nodes_split = []
        for i, text in enumerate(nodes_text):
            if i % 2 == 0:  # Always even splits are text nodes
                if text != "":
                    nodes_split.append(TextNode(text, TextType.TEXT))
            else:
                nodes_split.append(TextNode(text, text_type, url))
        new_nodes.extend(nodes_split)
    return new_nodes


def extract_markdown_links(text):
    match_pattern = r"(?<!!)\[[^\]]+\]\([^\)]+\)"
    matched_patterns = re.findall(match_pattern, text)
    matched_tuples = []
    for link in matched_patterns:
        data = link[1:-1].split("](")
        matched_tuples.append(tuple(data))
    return matched_tuples


def extract_markdown_images(text):
    match_pattern = r"!\[[^\]]+\]\([^\)]+\)"
    matched_patterns = re.findall(match_pattern, text)
    matched_tuples = []
    for image in matched_patterns:
        data = image[2:-1].split("](")
        matched_tuples.append(tuple(data))
    return matched_tuples


def split_nodes_link(old_nodes):
    match_pattern = r"(?<!!)\[[^\]]+\]\([^\)]+\)"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        link_text = extract_markdown_links(old_text)
        non_link_text_split = re.split(match_pattern, old_text)
        modified_nodes = []
        for i, node in enumerate(non_link_text_split):
            if node != "":
                modified_nodes.append(TextNode(node, TextType.TEXT))
            if len(link_text) > i:
                modified_nodes.append(
                    TextNode(link_text[i][0], TextType.LINK, link_text[i][1])
                )
        new_nodes.extend(modified_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    match_pattern = r"!\[[^\]]+\]\([^\)]+\)"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        old_text = old_node.text
        image_text = extract_markdown_images(old_text)
        non_image_text_split = re.split(match_pattern, old_text)
        modified_nodes = []
        for i, node in enumerate(non_image_text_split):
            if node != "":
                modified_nodes.append(TextNode(node, TextType.TEXT))
            if len(image_text) > i:
                modified_nodes.append(
                    TextNode(image_text[i][0], TextType.IMAGE, image_text[i][1])
                )
        new_nodes.extend(modified_nodes)
    return new_nodes
