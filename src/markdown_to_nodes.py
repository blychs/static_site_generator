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
        if t.startswith("```"):
            t = t.replace("```\n", "```")
            blocks.append(t)
            continue
        t = t.strip('\n')
        block_no_trailing = t.strip()
        block_no_trailing = block_no_trailing.strip('\n')
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


def olist_to_html(text):
    orig_lines = text.split('\n')
    def _re_lstrip(text):
        return re.sub(r"(?m)^\d+\. ", "", text)
    text_nodes = [text_to_textnodes(_re_lstrip(orig_line)) for orig_line in orig_lines]
    def _create_nodes(text_nodes):
        text_nodes_all = [text_node_to_html_node(text_node) for text_node in text_nodes]
        return ParentNode(tag="li", children=text_nodes_all)
    return list(map(_create_nodes, text_nodes))


def uolist_to_html(text):
    orig_lines = text.split('\n')
    text_nodes = [text_to_textnodes(orig_line.lstrip("- ")) for orig_line in orig_lines]
    def _create_nodes(text_nodes):
        text_nodes_all = [text_node_to_html_node(text_node) for text_node in text_nodes]
        return ParentNode(tag="li", children=text_nodes_all)
    return list(map(_create_nodes, text_nodes))


def markdown_to_html_node(text):
    output_node = ParentNode(tag="div", children=[])
    blocks = markdown_to_blocks(text)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            tag, contents = count_number_of_starting_hash(block)
            output_node.children.append(HTMLNode(tag, contents))
        elif block_type == BlockType.PARAGRAPH:
            block_textnodes = text_to_textnodes(block)
            text_nodes = [text_node_to_html_node(t) for t in block_textnodes]
            output_node.children.append(ParentNode(tag="p", children=text_nodes))
        elif block_type == BlockType.QUOTE:
            tag, contents = quote_to_html(block)
            content_nodes = text_to_textnodes(contents)
            html = [text_node_to_html_node(t) for t in content_nodes]
            output_node.children.append(ParentNode(tag=tag, children=html))
        elif block_type == BlockType.CODE:
            code_content = block.strip("```").lstrip()
            code_node = LeafNode(tag="code", value=code_content)
            output_node.children.append(ParentNode(tag="pre", children=[code_node]))
        elif block_type == BlockType.UNORDERED_LIST:
            elements = uolist_to_html(block)
            output_node.children.append(ParentNode(tag="ul", children=elements))
        elif block_type == BlockType.ORDERED_LIST:
            elements = olist_to_html(block)
            output_node.children.append(ParentNode(tag="ol", children=elements))
    return output_node
