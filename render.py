#!/usr/bin/env python3

import os
import markdown

from frontmatter import Frontmatter
from bin.govukify import govukify_markdown_output
from bin.jinja_setup import env, render
from bin.helpers import read_in_json
from digital_land_frontend.filters import make_link

from markdown.extensions.toc import TocExtension

# register jinja filters
env.filters["make_link"] = make_link

# set variables to make available to all templates
env.globals["staticPath"] = "https://digital-land.github.io"

# init markdown
md = markdown.Markdown(extensions=[TocExtension(toc_depth="2-3")])

def compile_markdown(md, s):
    html = md.convert(s)
    return govukify_markdown_output(html)

# making markdown compiler available to jinja templates
def markdown_filter(s):
    return compile_markdown(md, s)

env.filters["markdown"] = markdown_filter

def get_file_content(filename):
    file_content = Frontmatter.read_file(filename)
    return {
        "name": file_content["attributes"].get("name"),
        "status": file_content["attributes"].get("status"),
        "frontmatter": file_content["attributes"],
        "body": compile_markdown(md, file_content["body"]),
    }


def markdown_files_only(files, file_ext=".md"):
    return [f for f in files if f.endswith(file_ext)]


def add_to_index_list(l, page, path_part):
    page['url'] = path_part
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
    processed_top_level_pages = add_to_index_list(processed_top_level_pages, processed_page, top_level_page)
    render(f"{top_level_page}/index.html", content_template, content=processed_page)


# generate index page
render(f"index.html", index_template, top_level_pages=processed_top_level_pages)