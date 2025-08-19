import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def match_beginning_of_every_line(text, pattern):
    split_text = text.split("\n")
    for t in split_text:
        if not t.startswith(pattern):
            return False
    return True


def match_ordered_list(text):
    split_text = text.split("\n")
    for i, t in enumerate(split_text):
        if not t.startswith(f"{i+1}."):
            return False
    return True


def block_to_block_type(markdown_block: str) -> BlockType:
    if re.match(r"^#{1,6} ", markdown_block):
        return BlockType.HEADING
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    if match_beginning_of_every_line(markdown_block, ">"):
        return BlockType.QUOTE
    if match_beginning_of_every_line(markdown_block, "-"):
        return BlockType.UNORDERED_LIST
    if match_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
