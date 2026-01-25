
import unittest
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links
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

    def test_split_image_middle(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com) in the middle", 
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com"),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_start(self):
        node = TextNode(
            "![image](https://boot.dev) an image this was", TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://boot.dev"),
                TextNode(" an image this was", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com)", TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com"),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_image(self):
        node = TextNode("This is just text", TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_middle(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) in the middle", 
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_start(self):
        node = TextNode(
            "[link](https://boot.dev) a link this was", TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" a link this was", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_end(self):
        node = TextNode(
            "The link is at the end, here [link](https://boot.dev)", TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("The link is at the end, here ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com) and another [second link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_no_link(self):
        node = TextNode("This is just text", TextType.TEXT)

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
