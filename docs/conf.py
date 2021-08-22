import os
import sys

sys.path.insert(0, os.path.abspath("."))

project = "pfzy"
copyright = "2021, Kevin Zhuang"
author = "Kevin Zhuang"
version = "0.3.1"
release = "0.3.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "furo",
    "myst_parser",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "pfzy"

napoleon_include_init_with_doc = True
autosectionlabel_prefix_document = True
autodoc_typehints = "description"
autodoc_member_order = "bysource"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
