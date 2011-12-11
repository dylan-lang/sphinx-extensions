# encoding: utf-8
"""
dylandomain.py

Created by Dustin Voss on 2011-11-10.
Copyright (c) 2011 Open Dylan Maintainers. All rights reserved.
"""

import sys as SYS, os as OS, re as RE
from urlparse import *

import docutils.nodes as RST_NODES
import docutils.parsers.rst.directives as DIRECTIVES
import sphinx.addnodes as SPHINX_NODES

from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive
from sphinx.domains import Domain, Index
from sphinx.domains import ObjType
from sphinx.directives import DescDirective
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, GroupedField, TypedField


#
# DRM link support
#


def ensure_drm_index (filename):
    if DylanDomain.drm_index is None:
        DylanDomain.drm_index = {}
        with open(filename) as file_in:
            file_pattern = RE.compile(r'(\S+)\s+(.+)')
            for line in file_in:
                if line:
                    match = file_pattern.match(line)
                    if (match is not None):
                        key, value = match.groups()
                        DylanDomain.drm_index[key.lower()] = value
            
    
def drm_link (name, rawtext, text, lineno, inliner, options={}, context=[]):
    match = RE.match(r'^(\S+)$|^(.*) <(\S+)>$', text)
    if match:
        base_url = inliner.document.settings.env.app.config.dylan_drm_url
        ensure_drm_index(inliner.document.settings.env.app.config.dylan_drm_index)

        linkkey1, linktext, linkkey2 = match.groups()
        linkkey = linkkey1 or linkkey2
        linktext = (linktext or linkkey).strip()
        location = DylanDomain.drm_index.get(linkkey.lower(), linkkey)
        href = urljoin(base_url, location)

        set_classes(options)
        node = RST_NODES.reference(rawtext, linktext, refuri=href, **options)
        return [node], []
    else:
        msg = inliner.reporter.error(
            'Invalid syntax for :dylan:drm: role; '
            '`%s` should be like `ref` or `text <ref>`.' % text,
            line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    

#
# Dylan language directives
#


class DylanCurrentLibrary (Directive):
    """Sets up current library."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    
    def get_library_fullname (self, partial):
        return partial
        
    def set_current_library (self, library_tuple):
        env = self.state.document.settings.env
        env.temp_data['dylan:library'] = library_tuple[0]

    def run (self):
        name = self.get_library_fullname(self.arguments[0].strip)
        self.set_current_library(name)
        return []
    

class DylanCurrentModule (Directive):
    """Sets up current module."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    
    def get_module_fullname (self, partial):
        env = self.state.document.settings.env
        library = env.temp_data.get('dylan:library', None)
        if library is None:
            raise ValueError('No current library')
        return "%s:%s" % (library, partial)

    def set_current_module (self, module_tuple):
        env = self.state.document.settings.env
        env.temp_data['dylan:module'] = module_tuple[0]

    def run (self):
        name = self.get_module_fullname(self.arguments[0].strip)
        self.set_current_module(name)
        return []


class DylanDescDirective (DescDirective):
    """A documentable Dylan language object."""

    option_spec = {
        'noindex': DescDirective.option_spec['noindex'],
        'synopsis': DIRECTIVES.unchanged,
    }
    
    def fullname (self, partial):
        """Subclasses return the full, qualified name of this language element."""
        pass
    
    def handle_signature (self, sigs, signode):
        partial = sigs[0].strip
        fullname = self.fullname(partial)
        signode += SPHINX_NODES.desc_name(partial, partial)
        signode['fullname'] = fullname
        return (fullname, partial)
    
    def add_target_and_index (self, name_tuple, sigs, signode):
        # note target
        fullname = name_tuple[0]
        shortname = name_tuple[1]
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            inventory = self.env.domaindata['dylan']['objects']
            if fullname in inventory:
                self.state_machine.reporter.warning(
                    'Duplicate description of Dylan %s %s, ' % (self.objtype, fullname) +
                    'other instance in ' + self.env.doc2path(inventory[fullname][0]),
                    line=self.lineno)
            inventory[fullname] = (self.env.docname, self.objtype, shortname)

        # add index
        self.indexnode['entries'].append(('single', shortname, fullname, ''))

    
class DylanLibraryDesc (DylanDescDirective, DylanCurrentLibrary):
    """A Dylan library."""

    fullname = DylanCurrentLibrary.get_library_fullname
    
    def before_content (self):
        self.set_current_library(self.names[0])

        
class DylanModuleDesc (DylanDescDirective, DylanCurrentModule):
    """A Dylan module."""

    fullname = DylanCurrentModule.get_module_fullname
    
    def before_content (self):
        self.set_current_module(self.names[0])


class DylanBindingDesc (DylanDescDirective):
    """A Dylan binding."""
    
    def fullname (self, partial):
        env = self.state.document.settings.env
        module = env.temp_data.get('dylan:module', None)
        if module is None:
            raise ValueError('No current library or module')
        return "%s:%s" % (module, partial)


class DylanClassDesc (DylanBindingDesc):
    """A Dylan class."""

    doc_field_types = [
        GroupedField('superclass', label="Superclasses",
            names=('superclass', 'super')),
        GroupedField('keyword', label="Init-Keywords",
            names=('keyword', 'init-keyword'))
    ] + DylanBindingDesc.doc_field_types


#
# Dylan language indexing
#


class DylanObjectsIndex (Index):
    """
    Index for language objects.
    Basically looks like the following, assuming Sphinx adds "extras" to it
    in parentheses. ::
    
      tan (generic-function)
      format-out
        io:format-out (generic-function)
        system:cheap-io (function)
    """
    
    name = "apiindex"
    localname = "API Index"
    shortname = "api"
    
    def generate (self, docnames=None):
        content = {}

        # list of all objects, sorted by full name
        objects = sorted(self.domain.data['objects'].iteritems(),
                         key=lambda kv: "%s %s" % (kv[1][2].lower(), kv[0].lower()))

        # Add entries
        prev_shortname = ''
        num_toplevels = 0
        for fullname, (docname, objtype, shortname) in objects:
            if docnames and docname not in docnames:
                continue

            entries = content.setdefault(shortname[0].lower(), [])

            subtype = 0;
            if prev_shortname == shortname:
                if entries[-1][1] == 0:
                    # First subentry. Replace previous entry with an unlinked header.
                    prev_entry = entries[-1]
                    entries[-1] = [shortname, 1, "", "", "", "", ""]
                    # Duplicate previous entry as the first subentry, but use
                    # library and module instead of short name.
                    prev_fullname = prev_entry[3]
                    prev_entry[0] = prev_fullname.split(":")[0:-1]
                    prev_entry[1] = 2
                    entries.append(prev_entry)
                # Make the entry we are creating into a subentry.
                shortname = fullname.split(":")[0:-1]
                subtype = 2
            else:
                num_toplevels += 1

            entries.append([shortname, subtype, docname, fullname,
                            objtype, "", ""])

        # apply heuristics when to collapse index at page load:
        # only collapse if number of top level entries is larger than
        # number of subentries
        collapse = len(entries) - num_toplevels < num_toplevels

        # sort by first letter
        content = sorted(content.iteritems())

        return (content, collapse)


#
# Domain definition
#


class DylanDomain (Domain):
    name = 'dylan'
    label = 'Dylan'
    
    roles = {
        'drm': drm_link,
        'lib': XRefRole(),
        'mod': XRefRole(),
        'class': XRefRole(),
        # 'var': ,
        # 'const': ,
        # 'func': ,
        # 'meth': ,
        # 'gf': ,
        # 'macro': ,
    }
    
    directives = {
        'current-library': DylanCurrentLibrary,
        'current-module': DylanCurrentModule,
        'library': DylanLibraryDesc,
        'module': DylanModuleDesc,
        'class': DylanClassDesc,
        # 'variable': ,
        # 'constant': ,
        # 'function': ,
        # 'method': ,
        # 'generic-function': ,
        # 'macro': ,
    }
    
    object_types = {
        'library':  ObjType('library', 'lib'),
        'module':   ObjType('module', 'mod'),
        'class':    ObjType('class', 'class'),
        # 'variable': ObjType('variable', 'var'),
        # 'constant': ObjType('constant', 'const'),
        # 'function': ObjType('function', 'func'),
        # 'method':   ObjType('method', 'meth'),
        # 'generic-function': ObjType('generic function', 'gf'),
        # 'macro':    ObjType('macro', 'macro'),
    }
    
    initial_data = {
        'objects': {},      # fullname -> (docname, objtype, shortname)
    }
    
    indices = [
        DylanObjectsIndex
    ]
    
    drm_index = None
    
    def clear_doc(self, docname):
        pass
    
    def process_doc(self, env, docname, document):
        pass
        
    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        raise sphinx.environment.NoUri()
    
    def get_objects(self):
        for kv in self.data['objects'].iteritems():
            (fullname, (docname, objtype, shortname)) = kv
            yield (fullname, shortname, objtype, docname, fullname, 0)
        
    def get_type_name(self, type, primary=False):
        return super().get_type_name(type, primary)
    
    
def setup (app):
    default_index_path = OS.path.join(OS.path.dirname(__file__), 'drm_index.txt')
    app.add_config_value('dylan_drm_url', 'http://www.opendylan.org/books/drm/', 'html')
    app.add_config_value('dylan_drm_index', default_index_path, 'html')
    app.add_domain(DylanDomain)
