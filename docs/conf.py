import sys

sys.path.append("../")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FreeGSNKE'
copyright = '2023, authors'
author = 'authors'
release = '0.4.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks", 
    "sphinx.ext.intersphinx", 
    "sphinx.ext.mathjax", 
    "sphinx.ext.todo", 
    "sphinx.ext.viewcode", 
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
    'sphinx_rtd_dark_mode',
    # 'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting',
    # 'sphinxcontrib.bibtex',
    # 'sphinxcontrib.texfigure',
    'sphinx.ext.autosectionlabel',
    'sphinx_math_dollar',
]

bibtex_bibfiles = ['assets/refs.bib']
bibtex_default_style = 'unsrt'

nbsphinx_execute = 'never'
napoleon_google_docstring = False
napoleon_include_init_with_doc = True
napoleon_numpy_docstring = True
#autosummary_generate = True
#autoclass_content = "class"
#autodoc_default_flags = ["members", "no-special-members"]
#always_document_param_types = False
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
# source_suffix = ['.rst', '.ipynb']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language ="en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None
default_dark_mode = False
sphinx_tabs_disable_css_loading = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_theme_options = {
    # 'logo_only': True,
    'display_version': True,
    'navigation_depth': 1,
    "collapse_navigation": True

    # 'style_nav_header_background': '#C48EDC',
}
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
#html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
    'css/custom_tabs.css',
]

suppress_warnings = [ 'autosectionlabel.*', 'autodoc','autodoc.import_object']

# -- Extension configuration -------------------------------------------------