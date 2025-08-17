from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link 
from textnode import TextNode, TextType

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
