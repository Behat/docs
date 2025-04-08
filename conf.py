# -*- coding: utf-8 -*-

import sys, os
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer

lexers['php'] = PhpLexer(startinline=True)
extensions = [
   'notfound.extension',
   # Enables automatic linking to headings within the document within Sphinx
   'sphinx.ext.autosectionlabel',
   'sphinx_wagtail_theme'
]

source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'guides'

project = u'Behat'
copyright = u'2016 - %Y, Konstantin Kudryashov (@everzet)'

language = 'php'
highlight_language = 'php'

exclude_trees = []
exclude_patterns = []

htmlhelp_basename = 'behat'

html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
html_theme='sphinx_wagtail_theme'
html_theme_options = dict(
  # Base path for "Edit on Github" links
  github_url="https://github.com/Behat/docs/blob/v3.0/",
)

# If false, no index is generated.
# Since we are implementing search with Algolia DocSearch through ReadTheDocs,
# we do not need Sphinx to generate its own index. It might not hurt to keep
# the Sphinx index, but speeds up the build process.
html_use_index = False

# Don't show separate "view source" links on generated pages
html_show_sourcelink = False
