import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Get the markdown form a file
    with open(from_path) as f:
        file = f.read()
    with open(template_path) as t:
        template = t.read()

    # Turn the markdown into html
    node = markdown_to_html_node(file)
    html = node.to_html()

    title = extract_title(file)

    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)

    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as p:
        p.write(html_page)
