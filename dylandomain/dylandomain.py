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
from sphinx.util.nodes import make_refnode


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
            '`{0}` should be like `ref` or `text <ref>`.'.format(text),
            line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    

#
# Dylan language directives
#


def get_current_library (env):
    return env.temp_data.get('dylan:library', None)

def set_current_library (env, library):
    env.temp_data['dylan:library'] = library

def get_current_module (env):
    return env.temp_data.get('dylan:module', None)

def set_current_module (env, module):
    env.temp_data['dylan:module'] = module


def library_fullname (env, library):
    return library

def module_fullname (env, module, library=None):
    library = library or get_current_library(env)
    if library is None:
        raise ValueError('No current library for module {0}'.format(module))
    return "{0}:{1}".format(library, module)

def binding_fullname (env, binding, library=None, module=None):
    library = library or get_current_library(env)
    module = module or get_current_module(env)
    if library is None:
        raise ValueError('No current library for binding {0}'.format(binding))
    if module is None:
        raise ValueError('No current module for binding {0}'.format(binding))
    return "{0}:{1}:{2}".format(library, module, binding)

def fullname_parts (fullname):
    parts = fullname.split(':')
    if len(parts) == 3:
        return (parts[0], parts[1], parts[2])
    elif len(parts) == 2:
        return (parts[0], parts[1], None)
    elif len(parts) == 1 and parts[0] != '':
        return (parts[0], None, None)
    else:
        return (None, None, None)


def name_to_id (name):
    return name.replace(' ', '').replace('<', '[').replace('>', ']')


class DylanCurrentLibrary (Directive):
    """Sets up current library."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    
    def run (self):
        env = self.state.document.settings.env
        name = self.arguments[0].strip()
        set_current_library(env, name)
        return []
    

class DylanCurrentModule (Directive):
    """Sets up current module."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    
    def run (self):
        env = self.state.document.settings.env
        name = self.arguments[0].strip()
        set_current_module(env, name)
        return []


class DylanDescDirective (DescDirective):
    """A documentable Dylan language object."""

    display_name = None
    """
    Subclasses should set this to a string describing the type of language
    element they are.
    """
    
    option_spec = dict(DescDirective.option_spec.items() + {
        'synopsis': DIRECTIVES.unchanged,
    }.items())
    
    doc_field_types = [
        Field('discussion', label="Discussion", has_arg=False,
            names=('discussion', 'description')),
    ] + DescDirective.doc_field_types

    # It is not documented, but self.names is a series of tuples. Each tuple is
    # the result of handle_signature on a signature. A signature is a directive
    # argument; see get_signatures.

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    
    def fullname (self, partial):
        """
        Subclasses return the full, qualified name of this language element,
        including specializer.
        """
        return partial
    
    def annotations (self):
        """
        Subclasses return an iterable of strings annotating the language element,
        e.g. 'open', 'sealed'.
        """
        return []
    
    def handle_signature (self, sigs, signode):
        partial = sigs.strip()
        fullname = self.fullname(partial)
        annotations = self.annotations()

        # Language element name
        (library, module, binding) = fullname_parts(fullname)
        dispname = binding or module or library
        signode += SPHINX_NODES.desc_name(dispname, dispname)
        
        # Annotations
        annotations.append(self.display_name)
        annotlist = ' '.join(annotations)
        signode += RST_NODES.Text(' ')
        signode += SPHINX_NODES.desc_annotation(annotlist, annotlist)
        
        signode['fullname'] = fullname
        return (fullname, partial)
    
    def add_target_and_index (self, name_tuple, sigs, signode):
        # note target
        fullname = name_tuple[0]
        shortname = name_tuple[1]
        fullid = name_to_id(fullname)
        if fullid not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullid)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            inventory = self.env.domaindata['dylan']['objects']
            if fullid in inventory:
                self.state_machine.reporter.warning(
                    'Duplicate description of Dylan {0} {1}, other instance in {2}'
                        .format(self.objtype, fullname,
                                self.env.doc2path(inventory[fullid][0])),
                    line=self.lineno)
            inventory[fullid] = (self.env.docname, self.objtype,
                                 fullname, shortname, self.display_name)

        # add index
        (library, module, binding) = fullname_parts(fullname)
        indexname = unicode(binding or module or library)
        self.indexnode['entries'].append(('single', indexname, fullid, ''))
    
    def report_and_raise_error (self, error):
        src, srcline = self.state.state_machine.get_source_and_line()
        msg = self.state.reporter.warning(error.args[0], line=srcline)
        raise error

    
class DylanLibraryDesc (DylanDescDirective):
    """A Dylan library."""

    display_name = "library"

    def fullname (self, partial):
        env = self.state.document.settings.env
        try:
            return library_fullname(env, partial)
        except ValueError as ve:
            self.report_and_raise_error(ve)

    def before_content (self):
        env = self.state.document.settings.env
        if len(self.names) > 0 and len(self.names[0]) > 0:
            (lib, mod, bind) = fullname_parts(self.names[0][0])
            set_current_library(env, lib)

        
class DylanModuleDesc (DylanDescDirective):
    """A Dylan module."""

    display_name = "module"
    
    option_spec = dict(DylanDescDirective.option_spec.items() + {
        'library': DIRECTIVES.unchanged,
    }.items())

    def fullname (self, partial):
        env = self.state.document.settings.env
        library_option = self.options.get('library', None)
        try:
            return module_fullname(env, partial, library=library_option)
        except ValueError as ve:
            self.report_and_raise_error(ve)
    
    def before_content (self):
        env = self.state.document.settings.env
        if len(self.names) > 0 and len(self.names[0]) > 0:
            (lib, mod, bind) = fullname_parts(self.names[0][0])
            set_current_library(env, lib)
            set_current_module(env, mod)


class DylanBindingDesc (DylanDescDirective):
    """A Dylan binding."""
    
    option_spec = dict(DylanDescDirective.option_spec.items() + {
        'library': DIRECTIVES.unchanged,
        'module': DIRECTIVES.unchanged,
    }.items())

    doc_field_types = [
        Field('example', label="Example", has_arg=False,
            names=('example')),
    ] + DylanDescDirective.doc_field_types

    def fullname (self, partial):
        env = self.state.document.settings.env
        library_option = self.options.get('library', None)
        module_option = self.options.get('module', None)
        try:
            return binding_fullname(env, partial,
                    library=library_option, module=module_option)
        except ValueError as ve:
            self.report_and_raise_error(ve)
    
    def before_content (self):
        env = self.state.document.settings.env
        if len(self.names) > 0 and len(self.names[0]) > 0:
            (lib, mod, bind) = fullname_parts(self.names[0][0])
            set_current_library(env, lib)
            set_current_module(env, mod)


class DylanClassDesc (DylanBindingDesc):
    """A Dylan class."""

    display_name = "class"
    
    option_spec = dict(DylanBindingDesc.option_spec.items() + {
        'open': DIRECTIVES.flag,
        'primary': DIRECTIVES.flag,
        'free': DIRECTIVES.flag,
        'abstract': DIRECTIVES.flag,
        'sealed': DIRECTIVES.flag,
        'concrete': DIRECTIVES.flag,
        'instantiable': DIRECTIVES.flag,
        'uninstantiable': DIRECTIVES.flag
    }.items())

    doc_field_types = [
        Field('superclasses', label="Superclasses", has_arg=False,
            names=('supers', 'superclasses', 'super', 'superclass')),
        GroupedField('keyword', label="Init-Keywords",
            names=('keyword', 'init-keyword')),
        GroupedField('slots', label="Slots",
            names=('slot', 'getter')),
        Field('conditions', label="Conditions", has_arg=False,
            names=('conditions', 'exceptions', 'condition', 'exception',
                   'signals', 'throws')),
        Field('operations', label="Operations", has_arg=False,
            names=('operations', 'methods', 'functions')),
    ] + DylanBindingDesc.doc_field_types
   
    def annotations (self):
        annotations = []
        for key in ['open', 'primary', 'free', 'abstract', 'sealed', 'concrete',
                    'instantiable', 'uninstantiable']:
            if key in self.options:
                annotations.append(key)
        return annotations


class DylanFunctionDesc (DylanBindingDesc):
    """A Dylan function, method, or generic function."""

    doc_field_types = [
        TypedField('parameters', label="Parameters",
            names=('param', 'parameter')),
        GroupedField('values', label="Values",
            names=('value', 'val', 'retval', 'return')),
        Field('signature', label="Signature", has_arg=False,
            names=('sig', 'signature')),
        Field('conditions', label="Conditions", has_arg=False,
            names=('conditions', 'exceptions', 'signals', 'throws')),
    ] + DylanBindingDesc.doc_field_types


class DylanGenFuncDesc (DylanFunctionDesc):
    """A Dylan generic function."""

    display_name = "generic function"
    
    option_spec = dict(DylanFunctionDesc.option_spec.items() + {
        'sealed': DIRECTIVES.flag,
        'open': DIRECTIVES.flag
    }.items())
    
    def annotations (self):
        annotations = []
        for key in ['sealed', 'open']:
            if key in self.options:
                annotations.append(key)
        return annotations


class DylanMethodDesc (DylanFunctionDesc):
    """A Dylan method in a generic function."""

    display_name = "method"
    
    option_spec = dict(DylanFunctionDesc.option_spec.items() + {
        'specializer': DIRECTIVES.unchanged,
        'sealed': DIRECTIVES.flag,
    }.items())
    
    def fullname (self, partial):
        basename = super(DylanMethodDesc, self).fullname(partial)
        specializer = self.options['specializer']
        return "{0}({1})".format(basename, specializer)

    def annotations (self):
        annotations = []
        for key in ['sealed']:
            if key in self.options:
                annotations.append(key)
        return annotations


class DylanConstFuncDesc (DylanFunctionDesc):
    """A Dylan function not associated with a generic function."""

    display_name = "function"


class DylanConstOrVarDesc (DylanBindingDesc):
    """A Dylan constant or variable."""

    doc_field_types = [
        Field('type', label="Type",
            names=('type')),
        Field('value', label="Value",
            names=('value', 'val'))
    ] + DylanBindingDesc.doc_field_types


class DylanConstantDesc (DylanConstOrVarDesc):
    """A Dylan constant."""

    display_name = "constant"


class DylanVariableDesc (DylanConstOrVarDesc):
    """A Dylan variable."""

    display_name = "variable"


class DylanMacroDesc (DylanBindingDesc):
    """A Dylan macro."""

    display_name = "macro"

    option_spec = dict(DylanBindingDesc.option_spec.items() + {
        'statement': DIRECTIVES.flag,
        'function': DIRECTIVES.flag,
        'defining': DIRECTIVES.flag
    }.items())

    doc_field_types = [
        TypedField('parameters', label="Parameters",
            names=('param', 'parameter')),
        GroupedField('values', label="Values",
            names=('value', 'val', 'retval', 'return')),
        Field('call', label="Macro Call", has_arg=False,
            names=('call', 'macrocall', 'syntax'))
    ] + DylanBindingDesc.doc_field_types

    def annotations (self):
        annotations = []
        for key in ['statement', 'function', 'defining']:
            if key in self.options:
                annotations.append(key)
        return annotations


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
        io:format-out:format-out (generic function)
        system:cheap-io:format-out (function)
      min
        dylan:dylan:min(<integer>) (method)
        dylan:dylan:min(<float>) (method)
    """
    
    name = "apiindex"
    localname = "API Index"
    shortname = "api"
    
    def generate (self, docnames=None):
        # Dictionary of first letter -> array of entry records with that letter
        content = {}

        # list of all objects, sorted by short name then by library/module name
        objects = sorted(self.domain.data['objects'].iteritems(),
                         key=lambda kv: "{0} {1}".format(kv[1][3], kv[1][2]).lower())

        # Add entries
        prev_shortname = ''
        prev_fullname = ''
        num_toplevels = 0
        for (fullid, (docname, objtype, fullname, shortname, displaytype)) in objects:
            if docnames and docname not in docnames:
                continue

            # Find index character; omit leading non-alphanumerics.
            indexchar = None
            for char in shortname:
                if (char.isalnum()):
                    indexchar = char.upper()
                    break;
            indexchar = indexchar or shortname[0].upper()

            entries = content.setdefault(indexchar, [])

            # Use the last part of the full name in the index,
            # i.e. short name + specializer
            subtype = 0;
            (library, module, binding) = fullname_parts(fullname)
            indexname = binding or module or library
            
            if prev_shortname == shortname:
                # We have a duplicate name
                prev_entry = entries[-1]
                if prev_entry[1] == 0:
                    # Previous entry was a normal entry, so this is the first
                    # subentry. Replace previous entry with an unlinked header.
                    entries[-1] = [shortname, 1, "", "", "", "", ""]
                    
                    # Previous entry is now a header, so add the linkable original
                    # as the first subentry, but use the full name instead of the
                    # index name.
                    prev_entry[0] = prev_fullname
                    prev_entry[1] = 2
                    entries.append(prev_entry)

                # Make the entry we are creating into a subentry and use the
                # whole full name instead of just the last part.
                subtype = 2
                indexname = fullname

            else:
                # Keep track of how many top-level entries we have.
                num_toplevels += 1

            entries.append([indexname, subtype, docname, fullid, displaytype, "", ""])
            prev_shortname = shortname
            prev_fullname = fullname

        # apply heuristics as to when to collapse index at page load:
        # only collapse if number of top level entries is larger than
        # number of subentries
        collapse = len(content) - num_toplevels < num_toplevels

        # sort by index character
        content = sorted(content.iteritems())

        return (content, collapse)


#
# Dylan language cross-references
#


class DylanXRefRole (XRefRole):
    def process_link (self, env, refnode, has_explicit_title, title, target):
        """Stash the current library and module for later lookup."""
        refnode.dylan_curlibrary = get_current_library(env)
        refnode.dylan_curmodule = get_current_module(env)
        return (title, target)


def desc_link (name, rawtext, text, lineno, inliner, options={}, context=[]):
    """
    Rebuild rawtext and text to avoid default escaping/parsing behavior. We
    use [] instead of <> in targets.
    """
    match = RE.match(r'^(.+?) <(.+)>$|^(.+)$', text)
    if match:
        linktitle, linkkey1, linkkey2 = match.groups()
        linkkey = (linkkey1 or linkkey2)
        if linktitle is None:
            keyparts = linkkey.split(':')
            linktitle = keyparts[-1]
        
        esc_linktitle = linktitle.replace("<", r"\<").replace(">", r"\>")
        targ_linkkey = name_to_id(linkkey)
        new_text = "{0} <{1}>".format(linktitle, targ_linkkey)
        new_rawtext = ":{0}:`{1} <{2}>`".format(name, esc_linktitle, targ_linkkey)
        
        do_xref = DylanXRefRole()
        return do_xref(name, new_rawtext, new_text, lineno, inliner, options, context)
    else:
        msg = inliner.reporter.error(
            'Invalid syntax for :{0}: role; '
            '`{1}` should be like `ref` or `text <ref>`.'.format(name, text),
            line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    

#
# Domain definition
#


class DylanDomain (Domain):
    name = 'dylan'
    label = 'Dylan'
    
    roles = {
        'drm': drm_link,
        'lib': desc_link,
        'mod': desc_link,
        'class': desc_link,
        'var': desc_link,
        'const': desc_link,
        'func': desc_link,
        'meth': desc_link,
        'gf': desc_link,
        'macro': desc_link,
    }
    
    directives = {
        'current-library': DylanCurrentLibrary,
        'current-module': DylanCurrentModule,
        'library': DylanLibraryDesc,
        'module': DylanModuleDesc,
        'class': DylanClassDesc,
        'variable': DylanVariableDesc,
        'constant': DylanConstantDesc,
        'function': DylanConstFuncDesc,
        'method': DylanMethodDesc,
        'generic-function': DylanGenFuncDesc,
        'macro': DylanMacroDesc,
    }
    
    object_types = {
        'library':  ObjType('library', 'lib'),
        'module':   ObjType('module', 'mod'),
        'class':    ObjType('class', 'class'),
        'variable': ObjType('variable', 'var'),
        'constant': ObjType('constant', 'const'),
        'function': ObjType('function', 'func'),
        'method':   ObjType('method', 'meth'),
        'generic-function': ObjType('generic-function', 'gf'),
        'macro':    ObjType('macro', 'macro'),
    }
    
    initial_data = {
        'objects': {},
            # fullid -> (docname, objtype, fullname, shortname, displaytype)
            # fullid is fullname with <> replaced by [] and spaces removed
        'reflabels': {
            # label -> (docname, targetid)
            'dylan-apiindex': (name + DylanObjectsIndex.name,
                               DylanObjectsIndex.name)
        }
    }
    
    indices = [
        DylanObjectsIndex
    ]
    
    drm_index = None
    
    def clear_doc(self, docname):
        for fullid, (objects_docname, _, _, _, _) in self.data['objects'].items():
            if objects_docname == docname:
                del self.data['objects'][fullid]
    
    def process_doc(self, env, docname, document):
        pass
        
    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        if typ == 'ref':
            nodeargs = self.data['refnodes'].get(target, None)
            if nodeargs is not None:
                todocname = nodeargs[0]
                targetid = nodeargs[1]
                return make_refnode(builder, fromdocname, todocname, targetid, contnode)

        if typ in ['lib', 'mod', 'class', 'var', 'const', 'func', 'gf', 'meth', 'macro']:
            # Target will have been transformed to the standard ID format:
            # no spaces and <> changed to []. Additionally, the node will have
            # dylan_curlibrary and dylan_curmodule set. This is all done by
            # the role processing function and the DylanXRefRole class.
            colons = target.count(':')
            fulltarget = None
            library = node.dylan_curlibrary
            module = node.dylan_curmodule
            if colons == 2:
                fulltarget = target
            elif library is not None:
                library_id = name_to_id(library)
                if colons == 1:
                    fulltarget = "{0}:{1}".format(library_id, target)
                elif module is not None:
                    module_id = name_to_id(module)
                    if colons == 0:
                        fulltarget = "{0}:{1}:{2}".format(library_id, module_id, target)
            nodeargs = self.data['objects'].get(fulltarget, None)
            if nodeargs is not None:
                todocname = nodeargs[0]
                return make_refnode(builder, fromdocname, todocname, fulltarget, contnode)

        return None    
    
    def get_objects(self):
        for kv in self.data['objects'].iteritems():
            (fullid, (docname, objtype, fullname, shortname, displaytype)) = kv
            yield (fullname, shortname, objtype, docname, fullid, 0)
    
    
def setup (app):
    default_index_path = OS.path.join(OS.path.dirname(__file__), 'drm_index.txt')
    app.add_config_value('dylan_drm_url', 'http://www.opendylan.org/books/drm/', 'html')
    app.add_config_value('dylan_drm_index', default_index_path, 'html')
    app.add_domain(DylanDomain)
