import re
from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
from blocknode import BlockType, block_to_block_type
from utils import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)
from textnode import TextNode, TextType
from blocknode import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(text):
    text = text.split("\n\n")
    blocks = []
    for t in text:
        block_no_trailing = t.strip()
        if block_no_trailing != "":
            blocks.append(block_no_trailing)
    return blocks


def count_number_of_starting_hash(text):
    starter = re.match(r"^#{1,6} ", text)
    if not starter:
        raise ValueError("Text does not have proper format")
    return len(starter[0]) - 1


def quote_to_html(text):
    lines = text.split("\n")
    lines = [e.lstrip(">") for e in lines]
    return "blockquote", "\n".join(lines)


def markdown_to_html_nodes(text):
    output_node = ParentNode(tag="div", children=[])
    blocks = markdown_to_blocks(text)
    breakpoint()
    block_with_block_type = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            tag, contents = heading_number(block)
            output_node.children.append(HTMLNode(tag, contents))
        if block_type == BlockType.PARAGRAPH:
            block_textnodes = text_to_textnodes(block)
            text_nodes = [text_node_to_html_node(t) for t in block_textnodes]
            breakpoint()
            output_node.children.append(ParentNode(tag="p", children=text_nodes))
        if block_type == BlockType.QUOTE:
            tag, contents = quote_to_html(block)
            output_node.children.append(HTMLNode(tag, contents))
    breakpoint()


if __name__ == '__main__':
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    markdown_to_html_nodes(md)
