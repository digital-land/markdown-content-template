#!/usr/bin/env python3

import os
import markdown

from frontmatter import Frontmatter
from bin.jinja_setup import setup_jinja, render
from digital_land_frontend.markdown.filter import compile_markdown

from markdown.extensions.toc import TocExtension

# init jinja
env = setup_jinja()

# init markdown
md = markdown.Markdown(extensions=[TocExtension(toc_depth="2-3")])


def get_file_content(filename):
    file_content = Frontmatter.read_file(filename)
    return {
        "name": file_content["attributes"].get("name"),
        "status": file_content["attributes"].get("status"),
        "frontmatter": file_content["attributes"],
        "body": compile_markdown(file_content["body"], md),
    }


def markdown_files_only(files, file_ext=".md"):
    return [f for f in files if f.endswith(file_ext)]


def add_to_index_list(l, page, path_part):
    page["url"] = path_part
    l.append(page)
    return l


# get templates
index_template = env.get_template("index.html")
content_template = env.get_template("content.html")

content_dir = "content/"
top_level_pages = os.listdir(content_dir)
processed_top_level_pages = []

for top_level_page in top_level_pages:
    hasMultipleDatasets = False
    processed_page = get_file_content(f"{content_dir}{top_level_page}/index.md")
    processed_top_level_pages = add_to_index_list(
        processed_top_level_pages, processed_page, top_level_page
    )
    render(f"{top_level_page}/index.html", content_template, content=processed_page)


# generate index page
render(f"index.html", index_template, top_level_pages=processed_top_level_pages)