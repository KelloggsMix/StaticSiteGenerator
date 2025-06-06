import os
from pathlib import Path
from markdown_blocks import *

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[1:].strip()
        
    raise Exception("No H1 header found.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    print("MARKDOWN DEBUG:", markdown_content[:200])
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    to_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, default_basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path) and filename.endswith(".md"):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, default_basepath)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, default_basepath)