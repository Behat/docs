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
