# encoding: utf-8
"""
dylandomain.py

Created by Dustin Voss on 2011-11-10.
Copyright (c) 2011 Open Dylan Maintainers. All rights reserved.
"""

import sys, os, re, urlparse

from docutils import nodes
from docutils.parsers.rst.roles import set_classes

from sphinx.domains import Domain


def ensure_drm_index (filename):
    if DylanDomain.drm_index is None:
        DylanDomain.drm_index = {}
        with open(filename) as file_in:
            file_pattern = re.compile(r'(\S+)\s+(.+)')
            for line in file_in:
                if line:
                    match = file_pattern.match(line)
                    if (match is not None):
                        key, value = match.groups()
                        DylanDomain.drm_index[key.lower()] = value
            
    
def drm_link (name, rawtext, text, lineno, inliner, options={}, context=[]):
    match = re.match(r'^(\S+)$|^(.*) <(\S+)>$', text)
    if match:
        base_url = inliner.document.settings.env.app.config.dylan_drm_url
        ensure_drm_index(inliner.document.settings.env.app.config.dylan_drm_index)

        linkkey1, linktext, linkkey2 = match.groups()
        linkkey = linkkey1 or linkkey2
        linktext = (linktext or linkkey).strip()
        location = DylanDomain.drm_index.get(linkkey.lower(), linkkey)
        href = urlparse.urljoin(base_url, location)

        set_classes(options)
        node = nodes.reference(rawtext, linktext, refuri=href, **options)
        return [node], []
    else:
        msg = inliner.reporter.error(
            'Invalid syntax for :dylan:drm: role; '
            '`%s` should be like `ref` or `desc <ref>`.' % text,
            line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    

class DylanDomain (Domain):
    name = 'dylan'
    label = 'Dylan'
    roles = {
        'drm': drm_link
    }
    
    drm_index = None
    
    
def setup (app):
    default_index_path = os.path.join(os.path.dirname(__file__), 'drm_index.txt')
    app.add_config_value('dylan_drm_url', 'http://opendylan.org/books/drm/', 'html')
    app.add_config_value('dylan_drm_index', default_index_path, 'html')
    app.add_domain(DylanDomain)
