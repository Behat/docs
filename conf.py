# -*- coding: utf-8 -*-

import sys, os, sphinx_rtd_theme
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer

lexers['php'] = PhpLexer(startinline=True)
extensions = []

source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'

project = u'Behat'
copyright = u'2014, Konstantin Kudryashov (@everzet)'

version = '3.0'
release = '3.0.12'

language = 'php'
highlight_language = 'php'

exclude_trees = []
exclude_patterns = []

htmlhelp_basename = 'behat'

html_theme_path = ["_themes"]
html_theme = 'borg'

# Overriding the default Behat theme in order to have the default RTD theme.
# This allows us to check the entire documentation structure.
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]