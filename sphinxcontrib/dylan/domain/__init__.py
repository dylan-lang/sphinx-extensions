# encoding: utf-8
"""
Dylan

A domain package for Sphinx.

Created by Dustin Voss on 2011-11-10.
Copyright (c) 2011-2025 Dylan Hackers. All rights reserved.
"""

from .dylandomain import DylanDomain

def setup (app):
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_config_value
    app.add_config_value('dylan_drm_url', 'https://opendylan.org/books/drm/', 'html')
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_domain
    app.add_domain(DylanDomain)
