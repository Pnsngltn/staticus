import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_propeq(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

    def test_prop_none(self):
        node = HTMLNode()
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_prope_empty(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Me!", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), 
                         '<a href="https://www.boot.dev">Click Me!</a>'
                         )

    def test_leaf_no_a(self):
        node = LeafNode(None, "Just simple, plain Text.")
        self.assertEqual(node.to_html(), "Just simple, plain Text.")

    def test_leaf_value_error(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode("p", None)
            node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no Value")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_many_children(self):
        child_1 = LeafNode("p", "This paragraph")
        child_2 = LeafNode("p", "Another one")
        child_3 = LeafNode("a", "And a Clicky Thing", props={"href": "https://www.boot.dev"})
        parent_node = ParentNode("div", [child_1, child_2, child_3])
        self.assertEqual(
                parent_node.to_html(), 
                '<div><p>This paragraph</p><p>Another one</p><a href="https://www.boot.dev">And a Clicky Thing</a></div>'
                )

    def test_parent_with_props(self):
        child_node = LeafNode(None, "Just some Text")
        parent_node = ParentNode("div", [child_node], props={"class": "separator"})
        self.assertEqual(parent_node.to_html(), '<div class="separator">Just some Text</div>') 

    def test_parent_missing_tag(self):
        child_node = LeafNode(None, "Text")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no Tag")


    def test_parent_missing_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: missing Children")

    def test_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "Innermost Text")
        child_node = ParentNode("span", [grandchild_node], props={"class": "inner"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span class="inner"><b>Innermost Text</b></span></div>')
    
    def test_parent_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
