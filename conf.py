# -*- coding: utf-8 -*-

import sys, os
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer

lexers['php'] = PhpLexer(startinline=True)
extensions = []

source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'guides'

project = u'Behat'
copyright = u'2016, Konstantin Kudryashov (@everzet)'

language = 'php'
highlight_language = 'php'

exclude_trees = []
exclude_patterns = []

htmlhelp_basename = 'behat'

html_theme_path = ["_themes"]
html_theme = 'borg'
