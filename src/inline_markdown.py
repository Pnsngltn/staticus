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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # extract images and start spliting into nodes
            images = extract_markdown_images(node.text)

            if not images:
                new_nodes.append(node)
                continue

            original_text = node.text
            remaining_text = original_text

            for alt, link in images:

                text = remaining_text.split(f"![{alt}]({link})", 1)

                current_text = text[0]
                remaining_text = text[1]

                if current_text != "":

                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, link))

            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)

            if not links:
                new_nodes.append(node)
                continue

            original_text = node.text
            remaining_text = original_text

            for label, link in links:

                text = remaining_text.split(f"[{label}]({link})", 1)

                current_text = text[0]
                remaining_text = text[1]

                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                new_nodes.append(TextNode(label, TextType.LINK, link))

            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT),]

    # Extract Bold
    nodes = split_nodes_delimiter(nodes, "**" , TextType.BOLD)

    # Extract Italic
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Extract Code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Split images
    nodes = split_nodes_image(nodes)

    # Split links
    nodes = split_nodes_link(nodes)

    return nodes



