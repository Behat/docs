# -*- coding: utf-8 -*-

import sys, os
from sphinx.highlighting import lexers 
from pygments.lexers.web import PhpLexer 

lexers['php'] = PhpLexer(startinline=True)
extensions = []

templates_path = ['theme/_templates']

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

html_theme = 'scrolls'
pygments_style = 'monokai'

html_context = {
    'logo_name':     'behat',
    'menu_section':  'behat-docs'
}

html_static_path = ['theme/_static']
