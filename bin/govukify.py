#!/usr/bin/env python3


def govukify_markdown_output(html):
    html = html.replace("<p", '<p class="govuk-body"')
    html = html.replace("<h1", '<h1 class="govuk-heading-xl"')
    html = html.replace("<h2", '<h2 class="govuk-heading-l"')
    html = html.replace("<h3", '<h3 class="govuk-heading-m"')
    html = html.replace("<h4", '<h4 class="govuk-heading-s"')
    html = html.replace("<ul", '<ul class="govuk-list govuk-list--bullet"')
    html = html.replace("<pre>", '<pre class="hljs-container">')
    return html
