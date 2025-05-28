class HTMLNode():

    def  __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError("to_html method yet to be implemented")
    
    def props_to_html(self):
        result = ''
        if self.props:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag is None:
            return(f"{self.value}")
        if self.props is not None:
            print(f"{self.props}")
            return(f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
        else:
            return(f"<{self.tag}>{self.value}</{self.tag}>")
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and 
            self.value == other.value and 
            self.props == other.props)

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None or self.children == []:
            raise ValueError("Invalid HTML: parent node without children")
        leafs = ''
        for child in self.children:
            leafs += child.to_html()
        props_html = self.props_to_html() if self.props else ''
        return f"<{self.tag}{props_html}>{leafs}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

