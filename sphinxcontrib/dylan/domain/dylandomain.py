# encoding: utf-8
"""
dylandomain.py

Created by Dustin Voss on 2011-11-10.
Copyright (c) 2011-2016 Open Dylan Maintainers. All rights reserved.
"""

import sys as SYS, os as OS, re as RE
try:
    from urllib.parse import urljoin
except ImportError:
    from urllib.parse import urljoin

import docutils.nodes as RST_NODES
import docutils.parsers.rst.directives as DIRECTIVES
import sphinx.addnodes as SPHINX_NODES

from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive
from sphinx.domains import Domain, Index
from sphinx.domains import ObjType
from sphinx.directives import ObjectDescription
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, GroupedField, TypedField
from sphinx.util.nodes import make_refnode


from . import drmindex


#
# DRM link support
#


def drm_link (name, rawtext, text, lineno, inliner, options={}, context=[]):
    match = RE.match(r'^(.*)\s<(\S+)>$|^(.*)$', text, flags=RE.DOTALL)
    if match:
        base_url = inliner.document.settings.env.app.config.dylan_drm_url

        linktext, linkkey1, linkkey2 = match.groups()
        linkkey = linkkey1 or linkkey2
        linktext = (linktext or linkkey).strip()
        location = drmindex.lookup(linkkey)
        href = urljoin(base_url, location)

        set_classes(options)
        textnode = RST_NODES.literal(rawtext, linktext, classes=['xref', 'drm'])
        linknode = RST_NODES.reference('', '', refuri=href, **options)
        linknode += textnode
        return [linknode], []
    else:
        msg = inliner.reporter.error(
            'Invalid syntax for :dylan:drm: role; '
            '`{0}` should be like `ref` (one or more words) or `text <ref>`.'.format(text),
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
    name = name.replace('<', '[').replace('>', ']')
    return RE.sub(r'\s', '', name).lower()


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


# DylanDescDirective used to subclass DescDirective, which was deprecated and
# then removed completely. Hence the "Desc" in the name, I suspect. It's a good
# bet this should be called something like DylanObjectDescription or
# DylanLanguageObject now, but I'm being a little conservative about renaming
# everything until I know the code better. --cgay, 2023

class DylanDescDirective (ObjectDescription):
    """A documentable Dylan language object."""

    display_name = None
    """
    Subclasses should set this to a string describing the type of language
    element they are.
    """

    annotations = []
    """
    Subclasses should set this to an list of options that annotate the language
    element, such as 'sealed' or 'open' regarding classes. They must also be
    listed in option_spec, though not all options need to be annotations.
    """

    option_spec = dict(ObjectDescription.option_spec.items())
    option_spec.update(dict({'synopsis': DIRECTIVES.unchanged}.items()))

    doc_field_types = [
        Field('summary', label="Summary", has_arg=False,
              names=('summary')),
        Field('discussion', label="Discussion", has_arg=False,
              names=('discussion', 'description')),
        Field('seealso', label="See also", has_arg=False,
              names=('seealso',)),
    ] + ObjectDescription.doc_field_types

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

    def handle_signature (self, sigs, signode):
        signode['classes'].append('dylan-api')
        partial = sigs.strip()
        fullname = self.fullname(partial)

        # Language element name
        (library, module, binding) = fullname_parts(fullname)
        dispname = binding or module or library
        signode += SPHINX_NODES.desc_name(dispname, dispname)

        # Annotations
        annotations = []
        for opt in self.annotations:
            if opt in self.options:
                annot = self.options[opt]
                annotations.append((annot or opt).capitalize())
        annotations.append(self.display_name.capitalize())
        annotlist = ' '.join(annotations)
        signode += RST_NODES.Text(' ')
        signode += SPHINX_NODES.desc_annotation(annotlist, annotlist)

        signode['fullname'] = fullname
        return (fullname, partial, dispname)

    def add_target_and_index (self, name_tuple, sigs, signode):
        # note target
        fullname = name_tuple[0]
        shortname = name_tuple[1]
        specname = name_tuple[2]
        fullid = name_to_id(fullname)
        specid = name_to_id(specname)
        if fullid not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullid)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

            # Check if already defined
            inventory = self.env.domaindata['dylan']['objects']
            if fullid in inventory:
                self.state_machine.reporter.warning(
                    'Duplicate description of Dylan {0} {1}, other instance in {2}'
                        .format(self.objtype, fullname,
                                self.env.doc2path(inventory[fullid][0])),
                    line=self.lineno)

            # Add target
            inventory[fullid] = (self.env.docname, self.objtype,
                                 fullname, shortname, specname, self.display_name)

            # Add target by specname
            fullids = self.env.domaindata['dylan']['fullids']
            fullids.setdefault(specid, []).append(fullid)

        # add index
        indexentry = str(shortname)
        if shortname != specname:
            indexentry += "; {0}".format(specname)
        self.indexnode['entries'].append(('single', indexentry,
                                          fullid, '', None))

    def warn_and_raise_error (self, error):
        src, srcline = self.state.state_machine.get_source_and_line()
        msg = self.state.reporter.warning(error.args[0], line=srcline)
        raise error

    def err_and_raise_error (self, error):
        src, srcline = self.state.state_machine.get_source_and_line()
        msg = self.state.reporter.error(error.args[0], line=srcline)
        raise error


class DylanLibraryDesc (DylanDescDirective):
    """A Dylan library."""

    display_name = "library"

    def fullname (self, partial):
        env = self.state.document.settings.env
        try:
            return library_fullname(env, partial)
        except ValueError as ve:
            self.warn_and_raise_error(ve)

    def before_content (self):
        env = self.state.document.settings.env
        if len(self.names) > 0 and len(self.names[0]) > 0:
            (lib, mod, bind) = fullname_parts(self.names[0][0])
            set_current_library(env, lib)


class DylanModuleDesc (DylanDescDirective):
    """A Dylan module."""

    display_name = "module"

    option_spec = dict(DylanDescDirective.option_spec.items())
    option_spec.update(dict({'library': DIRECTIVES.unchanged}.items()))

    def fullname (self, partial):
        env = self.state.document.settings.env
        library_option = self.options.get('library', None)
        try:
            return module_fullname(env, partial, library=library_option)
        except ValueError as ve:
            self.warn_and_raise_error(ve)

    def before_content (self):
        env = self.state.document.settings.env
        if len(self.names) > 0 and len(self.names[0]) > 0:
            (lib, mod, bind) = fullname_parts(self.names[0][0])
            set_current_library(env, lib)
            set_current_module(env, mod)


class DylanBindingDesc (DylanDescDirective):
    """A Dylan binding."""

    annotations = [
        'adjectives'
    ] + DylanDescDirective.annotations

    option_spec = dict(DylanDescDirective.option_spec.items())
    option_spec.update(dict({
        'library': DIRECTIVES.unchanged,
        'module': DIRECTIVES.unchanged,
        'adjectives': DIRECTIVES.unchanged,
    }.items()))

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
                                    library=library_option,
                                    module=module_option)
        except ValueError as ve:
            self.warn_and_raise_error(ve)

    def before_content (self):
        env = self.state.document.settings.env
        if len(self.names) > 0 and len(self.names[0]) > 0:
            (lib, mod, bind) = fullname_parts(self.names[0][0])
            set_current_library(env, lib)
            set_current_module(env, mod)


class DylanClassDesc (DylanBindingDesc):
    """A Dylan class."""

    display_name = "class"

    annotations = [
        'open', 'primary', 'free', 'abstract', 'concrete', 'instantiable',
        'uninstantiable', 'sealed'
    ] + DylanBindingDesc.annotations

    option_spec = dict(DylanBindingDesc.option_spec.items())
    option_spec.update(dict({
        'open': DIRECTIVES.flag,
        'primary': DIRECTIVES.flag,
        'free': DIRECTIVES.flag,
        'abstract': DIRECTIVES.flag,
        'sealed': DIRECTIVES.flag,
        'concrete': DIRECTIVES.flag,
        'instantiable': DIRECTIVES.flag,
        'uninstantiable': DIRECTIVES.flag,
    }.items()))

    doc_field_types = [
        Field('superclasses', label="Superclasses", has_arg=False,
              names=('supers', 'superclasses', 'super', 'superclass')),
        TypedField('keyword', label="Init-Keywords",
                   names=('keyword', 'init-keyword')),
        GroupedField('slots', label="Slots",
                     names=('slot', 'getter')),
        Field('conditions', label="Conditions", has_arg=False,
              names=('conditions', 'exceptions', 'condition', 'exception',
                     'signals', 'throws')),
        Field('operations', label="Operations", has_arg=False,
              names=('operations', 'methods', 'functions')),
    ] + DylanBindingDesc.doc_field_types


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

    annotations = [
        'sealed', 'open'
    ] + DylanFunctionDesc.annotations

    option_spec = dict(DylanFunctionDesc.option_spec.items())
    option_spec.update(dict({
        'sealed': DIRECTIVES.flag,
        'open': DIRECTIVES.flag
    }.items()))


class DylanMethodDesc (DylanFunctionDesc):
    """A Dylan method in a generic function."""

    display_name = "method"

    annotations = [
        'sealed', 'open'
    ] + DylanFunctionDesc.annotations

    option_spec = dict(DylanFunctionDesc.option_spec.items())
    option_spec.update(dict({
        'specializer': DIRECTIVES.unchanged,
        'sealed': DIRECTIVES.flag,
        'open': DIRECTIVES.flag
    }.items()))

    def fullname (self, partial):
        basename = super(DylanMethodDesc, self).fullname(partial)
        specializer = self.options.get('specializer', None)
        if (specializer is None):
            e = ValueError('Method directive requires :specializer: option.')
            self.err_and_raise_error(e)
        return "{0}({1})".format(basename, specializer)


class DylanConstFuncDesc (DylanFunctionDesc):
    """A Dylan function not associated with a generic function."""

    display_name = "function"

class DylanPrimitiveDesc (DylanFunctionDesc):
    """A Dylan primitive."""

    display_name = "primitive"


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

class DylanTypeDesc (DylanConstOrVarDesc):
    """A Dylan type."""

    display_name ="type"

    doc_field_types = [
        Field('supertypes', label="Supertypes", has_arg=False,
              names=('supers', 'supertypes', 'super', 'supertype')),
        Field('equivalent', label="Equivalent", has_arg=False,
              names=('equivalent')),
        Field('operations', label="Operations", has_arg=False,
              names=('operations', 'methods', 'functions')),
    ] + DylanConstOrVarDesc.doc_field_types


class DylanVariableDesc (DylanConstOrVarDesc):
    """A Dylan variable."""

    display_name = "variable"

    annotations = [
        'thread'
    ] + DylanConstOrVarDesc.annotations

    option_spec = dict(DylanConstOrVarDesc.option_spec.items())
    option_spec.update(dict({
        'thread': DIRECTIVES.flag,
    }.items()))


class DylanMacroDesc (DylanBindingDesc):
    """A Dylan macro."""

    final_argument_whitespace = True

    display_name = "macro"

    annotations = [
        'statement', 'function', 'defining', 'macro-type'
    ] + DylanBindingDesc.annotations

    option_spec = dict(DylanBindingDesc.option_spec.items())
    option_spec.update(dict({
        'statement': DIRECTIVES.flag,
        'function': DIRECTIVES.flag,
        'defining': DIRECTIVES.flag,
        'macro-type': DIRECTIVES.unchanged,
    }.items()))

    doc_field_types = [
        TypedField('parameters', label="Parameters",
                   names=('param', 'parameter')),
        GroupedField('values', label="Values",
                     names=('value', 'val', 'retval', 'return')),
        Field('call', label="Macro Call", has_arg=False,
              names=('call', 'macrocall', 'syntax'))
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
        objects = sorted(self.domain.data['objects'].items(),
                         key=lambda kv: "{0} {1}".format(kv[1][3], kv[1][2]).lower())

        # Add entries
        prev_shortname = ''
        prev_fullname = ''
        num_toplevels = 0
        for (fullid, (docname, _, fullname, shortname, specname, displaytype)) in objects:
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
            # i.e. short name + specializer a.k.a. specname
            subtype = 0;
            indexname = specname

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
        content = sorted(content.items())

        return (content, collapse)


#
# Dylan language cross-references
#


class DylanXRefRole (XRefRole):
    def process_link (self, env, refnode, has_explicit_title, title, target):
        """
        Stash the current library and module for later lookup, and repair damage
        to title.
        """
        refnode.dylan_curlibrary = get_current_library(env)
        refnode.dylan_curmodule = get_current_module(env)
        title = title.replace("\x1A", "<")
        return (title, target)


def desc_link (name, rawtext, text, lineno, inliner, options={}, context=[]):
    """
    Rebuild rawtext and text to avoid default escaping/parsing behavior. We
    use [] instead of <> in targets and the SUB character instead of < in the
    title.
    """
    if name == 'dylan:meth':
        match = RE.match(r'^(.+)\s<(\S+\(.+\))>$|^(\S+\(.+\))$', text, flags=RE.DOTALL)
    elif name == 'dylan:macro':
        match = RE.match(r'^(.+)\s<((?:define\s+)?\S+)>$|^((?:define\s+)?\S+)$', text, flags=RE.DOTALL)
    else:
        match = RE.match(r'^(.+)\s<(\S+)>$|^(\S+)$', text, flags=RE.DOTALL)

    if match:
        linktitle, linkkey1, linkkey2 = match.groups()
        linkkey = (linkkey1 or linkkey2)
        if linktitle is None:
            keyparts = linkkey.split(':')
            linktitle = keyparts[-1]

        esc_linktitle = linktitle.replace("<", "\x1A")
        targ_linkkey = name_to_id(linkkey)
        new_text = "{0} <{1}>".format(esc_linktitle, targ_linkkey)
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
        'prim': desc_link,
        'type': desc_link,
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
        'primitive': DylanPrimitiveDesc,
        'macro': DylanMacroDesc,
        'type': DylanTypeDesc,
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
        'primitive': ObjType('primitive', 'prim'),
        'macro':    ObjType('macro', 'macro'),
        'type':     ObjType('type', 'type'),
    }

    initial_data = {
        'fullids': {},
            # specid -> [fullid, ...]
            # fullid is fullname with <> replaced by [] and spaces removed
            # specid is the specname with <> replaced by [] and spaces removed
        'objects': {},
            # fullid -> (docname, objtype, fullname, shortname, specname, displaytype)
            # fullid is fullname with <> replaced by [] and spaces removed
            # specname is the shortname plus specializer
        'reflabels': {
            # label -> (docname, targetid)
            'dylan-apiindex': (name + DylanObjectsIndex.name,
                               DylanObjectsIndex.name)
        }
    }

    indices = [
        DylanObjectsIndex
    ]

    def clear_doc(self, docname):
        for fullid, (objects_docname, _, _, _, specname, _) in list(self.data['objects'].items()):
            if objects_docname == docname:
                del self.data['objects'][fullid]
                specid = name_to_id(specname)
                if fullid in self.data['fullids'].get(specid, {}):
                    self.data['fullids'][specid].remove(fullid)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        if typ == 'ref':
            nodeargs = self.data['refnodes'].get(target, None)
            if nodeargs is not None:
                todocname = nodeargs[0]
                targetid = nodeargs[1]
                return make_refnode(builder, fromdocname, todocname, targetid, contnode)

        if typ in ['lib', 'mod', 'class', 'var', 'const', 'func', 'gf', 'meth', 'macro', 'type']:
            # Target will have been transformed to the standard ID format:
            # no spaces and <> changed to []. Additionally, the node will have
            # dylan_curlibrary and dylan_curmodule set if possible. This is all
            # done by the role processing function and the DylanXRefRole class.
            colons = target.count(':')
            fulltarget = None

            if hasattr(node, "dylan_curlibrary"):
                library = node.dylan_curlibrary
            else:
                library = None

            if hasattr(node, "dylan_curmodule"):
                module = node.dylan_curmodule
            else:
                module = None

            # Use current library and module
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

            # Fetch link info based on current library and module and passed target
            nodeargs = self.data['objects'].get(fulltarget, None)

            # Can't find it that way; check the unique shortname list
            if nodeargs is None and colons == 0:
                targlist = self.data['fullids'].get(target, [])
                if len(targlist) == 1:
                    fulltarget = targlist[0]
                    nodeargs = self.data['objects'].get(fulltarget, None)

            # Found it; make a link.
            if nodeargs is not None:
                todocname = nodeargs[0]
                return make_refnode(builder, fromdocname, todocname, fulltarget, contnode)

        return None

    def get_objects(self):
        # These objects go into the objects.inv which is used
        # for intersphinx. This also feeds into tools like doc2dash
        # which only expect a fairly standard set of object types.
        REMAP_TYPES = {
            'generic-function': 'function',
            'primitive': 'function'
        }
        for kv in self.data['objects'].items():
            (fullid, (docname, objtype, fullname, shortname, specname, displaytype)) = kv
            objtype = REMAP_TYPES.get(objtype, objtype)
            yield (shortname, specname, objtype, docname, fullid, 0)
