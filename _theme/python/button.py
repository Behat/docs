# Basic sphinx plugin to support button-style links from RST
# Borrowed from https://stackoverflow.com/questions/25088113/make-a-css-button-a-link-in-sphinx
# and https://github.com/conda/conda-docs/blob/04613488d57688d77b0bc20618b9a4d5b56947ed/web/source/conf.py
# with some alterations to allow customisation of the button CSS class and to convert `/` urls to be relative
# to the html_baseurl for support on ReadTheDocs etc and fixes for newer Sphinx versions.
from __future__ import absolute_import
from docutils import nodes
import jinja2
from docutils.parsers.rst.directives import unchanged
from sphinx.util.docutils import SphinxDirective

BUTTON_TEMPLATE = jinja2.Template(u"""
<a class="{{ btn_class }}" href="{{ link }}">
    {{ text }}
</a>
""")

# placeholder node for document graph
class button_node(nodes.General, nodes.Element):
    pass

class ButtonDirective(SphinxDirective):
    required_arguments = 0

    option_spec = {
        'class': unchanged,
        'text': unchanged,
        'link': unchanged,
    }

    # this will execute when your directive is encountered
    # it will insert a button_node into the document that will
    # get visisted during the build phase
    def run(self):
        # Absolute local URLs should be made relative to the html_baseurl for the site
        # Otherwise they will not work on ReadTheDocs
        url = self.options['link']
        if url.startswith('/'):
          url = self.config.html_baseurl + url.lstrip('/')

        if 'class' in self.options:
          btn_class = self.options['class']
        else:
          btn_class = 'btn btn-primary'

        node = button_node()
        node['text'] = self.options['text']
        node['btn_class'] = btn_class
        node['link'] = url
        return [node]

# build phase visitor emits HTML to append to output
def html_visit_button_node(self, node):
    html = BUTTON_TEMPLATE.render(text=node['text'], btn_class=node['btn_class'], link=node['link'])
    self.body.append(html)
    raise nodes.SkipNode

# note, not defining visitors for text or manpage etc format as we only output HTML for Behat

def setup(app):
    app.add_node(button_node,
                 html=(html_visit_button_node, None))
    app.add_directive('button', ButtonDirective)