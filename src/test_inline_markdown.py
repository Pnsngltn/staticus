
import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold_delimiter(self):
        node = TextNode("This is text with **bold text** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD), 
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_double_bold(self):
        node = TextNode("This is plain text, **this is bold**, **and this is also bold**, but this isn't", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is plain text, ", TextType.TEXT),
                TextNode("this is bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("and this is also bold", TextType.BOLD),
                TextNode(", but this isn't", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_italic_delimiter(self):
        node = TextNode("This is normal and _italic text_ respectively", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is normal and ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" respectively", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is just plain text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_invalid_markdown(self):
        node = TextNode("This is invalid `syntax for a code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_two_images(self):
        matches = extract_markdown_images(
            "This is text with more that one ![image one](https://i.imgur.com/zjjcJKZ.png) and this is another ![image two](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image one", "https://i.imgur.com/zjjcJKZ.png"), ("image two", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
            )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_two_links(self):
        matches = extract_markdown_links(
            "This is text with [one link](https://www.boot.dev) and [another](https://www.boot.dev)"
            )
        self.assertListEqual([("one link", "https://www.boot.dev"), ("another", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()
