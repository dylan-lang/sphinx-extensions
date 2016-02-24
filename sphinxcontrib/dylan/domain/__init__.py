# encoding: utf-8
"""
Dylan

A domain package for Sphinx.

Created by Dustin Voss on 2011-11-10.
Copyright (c) 2011-2016 Open Dylan Maintainers. All rights reserved.
"""

from .dylandomain import DylanDomain

def setup (app):
    app.add_config_value('dylan_drm_url', 'http://opendylan.org/books/drm/', 'html')
    app.add_domain(DylanDomain)
