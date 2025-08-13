class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception(NotImplementedError)

    def props_to_html(self):
        if self.props is None:
            return None
        output_html = ""
        for prop in self.props:
            if output_html != "":
                output_html += " "
            output_html += f'{prop}="{self.props[prop]}"'
        return output_html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
