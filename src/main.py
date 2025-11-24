# from textnode import TextNode, TextType
import os
import shutil
from utils import copy_src_dst
from generate_html import generate_pages_recursive


def main():
    if os.path.exists('public'):
        shutil.rmtree('public')
    copy_src_dst("static", "public")
    generate_pages_recursive('content', 'template.html', 'public')

    


if __name__ == "__main__":
    main()
