# from textnode import TextNode, TextType
import os
import shutil
import sys
from utils import copy_src_dst
from generate_html import generate_pages_recursive


def main():
    if os.path.exists('public'):
        shutil.rmtree('public')
    copy_src_dst("static", "docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive('content', 'template.html', 'docs', basepath=basepath)

    


if __name__ == "__main__":
    main()
