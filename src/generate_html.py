import os
from markdown_to_nodes import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        line_strp = line.strip()
        if line_strp.startswith("#") and not line_strp.startswith("##"):
            return line_strp.lstrip("#").strip()
    raise Exception("No valid title")


def generate_html(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )
    with open(from_path, 'r') as f:
        md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w') as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        new_dest = dest_dir_path.rstrip(".md") + ".html"
        generate_html(dir_path_content, template_path, new_dest)
        return
    contents = os.listdir(dir_path_content)
    for content in contents:
        new_src = os.path.join(dir_path_content, content)
        new_dest = os.path.join(dest_dir_path, content)
        new_dest_dir = os.path.dirname(dest_dir_path)
        generate_pages_recursive(new_src, template_path, new_dest)
