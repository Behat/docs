# -*- coding: utf-8 -*-

import sys, os
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer

lexers['php'] = PhpLexer(startinline=True)

# Add our custom python path to the system search path so that sphinx can find extensions there
sys.path.insert(0, os.path.abspath('./_theme/python'))

extensions = [
   'notfound.extension',
   # Enables automatic linking to headings within the document within Sphinx
   'sphinx.ext.autosectionlabel',
   'sphinx_wagtail_theme',
   # Enables a .. button:: directive to render a link as a button e.g. on homepage. Use sparingly.
   'button',
   # Installs and runs lightningcss to bundle and minify our custom CSS
   'lightningcss',
]

source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'

project = u'Behat'
copyright = u'2016 - %Y, Konstantin Kudryashov (@everzet)'

language = 'php'
highlight_language = 'php'

exclude_trees = []
exclude_patterns = []

htmlhelp_basename = 'behat'

# Files in these paths are copied to the _static output directory e.g. theme/static/img/file.png
# will become "/_static/img/file.png". They will overwrite any file from the theme with the same
# name.
html_static_path = ['_theme/static']

# CSS files here are relative to html_static_path (or absolute urls)
html_css_files = [
  'https://fonts.googleapis.com/css?family=Comfortaa&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800',
  'css/behat-docs.css',
]

# Files in these paths override templates provided by the theme
templates_path = ['_theme/templates']

html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
html_theme='sphinx_wagtail_theme'
html_theme_options = dict(
  # Navbar branding
  project_name = "Behat",
  logo = 'img/behat-b-2x-white.png',
  logo_alt = 'Behat',
  logo_url = '/',
  logo_width = 36,
  logo_height = 50,

  # Base path for "Edit on GitHub" links
  github_url="https://github.com/Behat/docs/blob/v3.0/",

  # Global header / footer links as text|target
  header_links=', '.join([
    f"Releases|{html_baseurl}releases.html",
    'GitHub|https://github.com/Behat/Behat'
  ]),
  footer_links=', '.join([
  ])
)

# If false, no index is generated.
# Since we are implementing search with Algolia DocSearch through ReadTheDocs,
# we do not need Sphinx to generate its own index. It might not hurt to keep
# the Sphinx index, but speeds up the build process.
html_use_index = False

# Don't show separate "view source" links on generated pages
html_show_sourcelink = False
