from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(markdown):
    # Split block at first space
    parts = markdown.split(" ", 1)
    # Split into lines
    lines = markdown.split("\n")

    # Check if it's a code block
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    # Check if it's a heading
    if len(parts) == 2:
        prefix = parts[0]
        if prefix == "#" * len(prefix) and 1 <= len(prefix) <= 6:
            return BlockType.HEADING
    # Check if it's a quote
    if all(line.startswith(">") or line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    # Check if it's an unordered_list
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    # Check if it's an ordered_list
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    blocks = []

    for section in sections:
        section = section.strip()

        if section != "":
            blocks.append(section)

    return blocks


