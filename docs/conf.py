# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LemLib'
copyright = '2024, Liam Teale'
author = 'Liam Teale'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'breathe',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx.ext.linkcode'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"

html_theme_options = {
    "source_repository": "https://github.com/lemlib/lemlib/",
    "source_branch": "master",
    "source_directory": "docs/",

    "light_css_variables": {
        "color-brand-primary": "#00C852",
        "color-brand-content": "#00C852",
    },

    "dark_css_variables": {
        "color-brand-primary": "#00C852",
        "color-brand-content": "#00C852",

    },
    'accent_color': 'grass'
}

html_static_path = ['_static']


breathe_projects = {"LemLib": "xml/"}

breathe_projects_source = {
    "LemLib" : (
        "../", ["include/lemlib", "include/lemlib/chassis"]
    )
}

breathe_default_project = "LemLib"

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]



# Run doxygen for the readthedocs build

import subprocess, os

read_the_docs_build = os.environ.get('READTHEDOCS', None) == 'True'

if read_the_docs_build:
     subprocess.call('cd ../doxygen; doxygen', shell=True)


import os
import xml.etree.ElementTree as ET

# Customize these
GITHUB_BASE_URL = "https://github.com/lemlib/lemlib/blob/stable/"
PROJECT_ROOT = os.path.abspath("../../")  # adjust to match root
DOXYGEN_XML_DIR = os.path.abspath("docs/xml")

def find_file_and_line(name):
    """
    Find the source file and line number for a function or class using Doxygen XML.
    """
    for filename in os.listdir(DOXYGEN_XML_DIR):
        if not filename.endswith(".xml"):
            continue
        path = os.path.join(DOXYGEN_XML_DIR, filename)
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            continue

        root = tree.getroot()

        # <compounddef kind="class"> or <memberdef kind="function">
        for member in root.findall(".//memberdef"):
            if member.get("kind") not in ("function", "class", "variable"):
                continue

            qualified = member.findtext("qualifiedname")
            if qualified and qualified.endswith(name):
                location = member.find("location")
                if location is not None:
                    file_path = location.get("file")
                    line = location.get("line")
                    return file_path, line
    return None, None

def linkcode_resolve(domain, info):
    print("linkcode_resolve CALLED")
    print(f"domain = {domain}, fullname = {info.get('fullname')}")

    if domain != "cpp":
        return None

    fullname = info.get("fullname")
    if not fullname:
        return None

    file_path, line = find_file_and_line(fullname)
    if not file_path or not line:
        return None

    # Normalize path for GitHub (strip local path to make relative)
    rel_path = os.path.relpath(file_path, PROJECT_ROOT).replace("\\", "/")

    return f"{GITHUB_BASE_URL}{rel_path}#L{line}"

