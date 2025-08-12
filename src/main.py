from textnode import TextNode, TextType


def main():
    text_node = TextNode("This is some text", TextType.LINK, "www.google.com")
    print(text_node)


if __name__ == "__main__":
    main()
