"""Configuration file for the Sphinx documentation builder."""

import os

# -- Project information -----------------------------------------------------
project = "awesome-foamlib"
copyright_text = "2025, Tetsuo Koyama"
author = "Tetsuo Koyama"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_gallery.gen_gallery",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Sphinx Gallery configuration --------------------------------------------
sphinx_gallery_conf = {
    "examples_dirs": "../examples",
    "gallery_dirs": "auto_examples",
    "filename_pattern": r"\.py$",
    "ignore_pattern": r"(__init__|conf)\.py",
    "download_all_examples": False,
    "plot_gallery": True,
    "abort_on_example_error": False,  # Don't fail build on example errors
    "matplotlib_animations": False,
    "image_scrapers": ("matplotlib",),  # Only scrape matplotlib figures
    "reset_modules": ("matplotlib", "seaborn"),
}

# Configure PyVista for headless rendering on ReadTheDocs
if os.environ.get("READTHEDOCS") == "True":
    # Set PyVista to off-screen rendering for headless environment
    try:
        import pyvista as pv

        pv.OFF_SCREEN = True
        pv.start_xvfb()
    except (ImportError, OSError):
        pass  # PyVista not available or xvfb not available

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}
