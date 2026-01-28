import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_leading_blank_line(self):
        md = """

            This is `code` and this is **bold**

            This is a new line with _italic_.
            """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is `code` and this is **bold**",
                "This is a new line with _italic_.",
            ],
        )

    def test_trailing_blank_line(self):
        md = """
This is **bold**
This is _italic_

This is `code` on a new block

"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bold**\nThis is _italic_",
                "This is `code` on a new block",
            ],
        )

    def test_multiple_blank_lines(self):
        md = """
This is normal text
But this is **bold**


_This is italic_
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is normal text\nBut this is **bold**",
                "_This is italic_",
            ],
        )
class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        md = "This is just text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)
    def test_heading(self):
        md = "### This is a Heading"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)
    def test_code(self):
        md = "```\nThis is a code block\n```"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)
    def test_quote(self):
        md = "> this is a quote.\n> this is part of it"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)
    def test_ulist(self):
        md = "- this is an item\n- this is another"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ULIST)
    def test_olist(self):
        md = "1. item\n2. items\n3. items"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.OLIST)
        
if __name__ == "__main__":
    unittest.main()
