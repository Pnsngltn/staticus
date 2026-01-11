import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            slices = node.text.split(delimiter)

            if len(slices) % 2 == 0:
                raise Exception("invalid markdown")
            else:
                for index, item in enumerate(slices):
                    if item == "":
                        continue
                    if index % 2 == 0:
                        # Text
                        new_nodes.append(TextNode(item, TextType.TEXT))
                        continue
                    else:
                        # Modifier
                        new_nodes.append(TextNode(item, text_type))
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links
