#!/usr/bin/env python3

import os
import jinja2

from digital_land_frontend.filters import make_link
from digital_land_frontend.markdown.filter import markdown_filter

# output directory
docs = "docs/"

def render(path, template, **kwargs):
    path = os.path.join(docs, path)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(template.render(**kwargs))


def setup_jinja():
    # register templates
    multi_loader = jinja2.ChoiceLoader(
        [
            jinja2.FileSystemLoader(searchpath="./templates"),
            jinja2.PrefixLoader(
                {
                    "digital-land-frontend": jinja2.PackageLoader("digital_land_frontend"),
                    "govuk-jinja-components": jinja2.PackageLoader(
                        "govuk_jinja_components"
                    ),
                }
            ),
        ]
    )

    env = jinja2.Environment(loader=multi_loader, autoescape=True)

    # register jinja filters
    env.filters["make_link"] = make_link
    env.filters["markdown"] = markdown_filter

    # set variables to make available to all templates
    env.globals["staticPath"] = "https://digital-land.github.io"

    return env
