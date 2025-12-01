import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_propeq(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

    def test_propnone(self):
        node = HTMLNode()
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_propeempty(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")
