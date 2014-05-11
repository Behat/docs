# -*- coding: utf-8 -*-

import sys, os
from sphinx.highlighting import lexers 
from pygments.lexers.web import PhpLexer 

lexers['php'] = PhpLexer(startinline=True)

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'behat documentation'
copyright = u'2014, Konstantin Kudryashov (@everzet)'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'php'
highlight_language = 'php'

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []
