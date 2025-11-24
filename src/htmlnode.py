class HTMLNode:
    """HTMLNode, requires tag, value, children and props.

    Attributes
    ----------
    tag : string (optional)
        string with the tag that corresponds.
    value : string (optional)
        string with the contents of the node.
    children : list[HTMLNode | LeafNode | ParentNode]
        List of HTML nodes that are children of the previous node.
    props : dict[str, str]
        List of properties to add to the html tags when parsing.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception(NotImplementedError)

    def props_to_html(self):
        if self.props is None:
            return ""
        output_html = ""
        for prop in self.props:
            if output_html != "":
                output_html += " "
            output_html += f'{prop}="{self.props[prop]}"'
        return output_html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes *must* have a value")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        if len(self.tag) > 0 and len(props_html) > 0:
            props_html = " " + props_html
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if isinstance(children, list):
            super().__init__(tag, None, children, props)
        else:
            child = [].append(children)
            super().__init__(tag, None, child, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node has to have tags")
        if self.children is None:
            raise ValueError("Parent node has to have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        props_html = self.props_to_html()
        if len(self.tag) > 0 and len(props_html) > 0:
            props_html = " " + props_html
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
        )
