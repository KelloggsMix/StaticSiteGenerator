import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.google.com")
        self.assertEqual("TextNode(This is a text node, text, https://www.google.com)", repr(node))
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_normal_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.google.com", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
        
    def test_text(self):
        node = TextNode("This is just text", TextType.TEXT)
        expected = LeafNode(None, "This is just text", None)
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_bold_text(self):
        node = TextNode("This is bold text", TextType.BOLD)
        expected = LeafNode("b", "This is bold text", None)
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_link_text(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        expected = LeafNode("a", "This is a link", {"href": "https://www.google.com"})
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_image_text(self):
        node = TextNode("This is an image of a cat", TextType.IMAGE, "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg")
        expected = LeafNode("img", "", {"src": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg", "alt": "This is an image of a cat"})
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_wrong_type_text(self):
        node = TextNode("Wrong type", "wrong type", "https://www.google.com")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__name__":
    unittest.main()