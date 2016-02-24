# encoding: utf-8
""",
drmindex.py

Copyright (c) 2011-2016 Open Dylan Maintainers. All rights reserved.
""",

index = {
  "odd?": "Arithmetic_Operations#odd_",
  "even?": "Arithmetic_Operations#even_",
  "zero?": "Arithmetic_Operations#zero_",
  "positive?": "Arithmetic_Operations#positive_",
  "negative?": "Arithmetic_Operations#negative_",
  "integral?": "Arithmetic_Operations#integral_",
  "+": "Arithmetic_Operations#addition",
  "*": "Arithmetic_Operations#multiplication",
  "-": "Arithmetic_Operations#subtraction",
  "/": "Arithmetic_Operations#division",
  "negative": "Arithmetic_Operations#negative",
  "floor": "Arithmetic_Operations#floor",
  "ceiling": "Arithmetic_Operations#ceiling",
  "round": "Arithmetic_Operations#round",
  "truncate": "Arithmetic_Operations#truncate",
  "floor/": "Arithmetic_Operations#floor_div",
  "ceiling/": "Arithmetic_Operations#ceiling_div",
  "round/": "Arithmetic_Operations#round_div",
  "truncate/": "Arithmetic_Operations#truncate_div",
  "modulo": "Arithmetic_Operations#modulo",
  "remainder": "Arithmetic_Operations#remainder",
  "^": "Arithmetic_Operations#exponentiation",
  "abs": "Arithmetic_Operations#abs",
  "logior": "Arithmetic_Operations#logior",
  "logxor": "Arithmetic_Operations#logxor",
  "logand": "Arithmetic_Operations#logand",
  "lognot": "Arithmetic_Operations#lognot",
  "logbit?": "Arithmetic_Operations#logbit_",
  "ash": "Arithmetic_Operations#ash",
  "lcm": "Arithmetic_Operations#lcm",
  "gcd": "Arithmetic_Operations#gcd",
  "identity": "Coercing_and_Copying_Objects#identity",
  "values": "Coercing_and_Copying_Objects#values",
  "as": "Coercing_and_Copying_Objects#as",
  "as-uppercase": "Coercing_and_Copying_Objects#as-uppercase",
  "as-uppercase!": "Coercing_and_Copying_Objects#as-uppercase.",
  "as-lowercase": "Coercing_and_Copying_Objects#as-lowercase",
  "as-lowercase!": "Coercing_and_Copying_Objects#as-lowercase.",
  "shallow-copy": "Coercing_and_Copying_Objects#shallow-copy",
  "type-for-copy": "Coercing_and_Copying_Objects#type-for-copy",
  "<collection>": "Collection_Classes#collection",
  "<explicit-key-collection>": "Collection_Classes#explicit-key-collection",
  "<sequence>": "Collection_Classes#sequence",
  "<mutable-collection>": "Collection_Classes#mutable-collection",
  "<mutable-explicit-key-collection>": "Collection_Classes#mutable-explicit-key-collection",
  "<mutable-sequence>": "Collection_Classes#mutable-sequence",
  "<stretchy-collection>": "Collection_Classes#stretchy-collection",
  "<array>": "Collection_Classes#array",
  "<vector>": "Collection_Classes#vector",
  "<simple-vector>": "Collection_Classes#simple-vector",
  "<simple-object-vector>": "Collection_Classes#simple-object-vector",
  "<stretchy-vector>": "Collection_Classes#stretchy-vector",
  "<deque>": "Collection_Classes#deque",
  "<list>": "Collection_Classes#list",
  "<pair>": "Collection_Classes#pair",
  "<empty-list>": "Collection_Classes#empty-list",
  "<range>": "Collection_Classes#range",
  "<string>": "Collection_Classes#string",
  "<byte-string>": "Collection_Classes#byte-string",
  "<unicode-string>": "Collection_Classes#unicode-string",
  "<table>": "Collection_Classes#table",
  "<object-table>": "Collection_Classes#object-table",
  "empty?": "Collection_Operations#empty_",
  "size": "Collection_Operations#size",
  "size-setter": "Collection_Operations#size-setter",
  "rank": "Collection_Operations#rank",
  "row-major-index": "Collection_Operations#row-major-index",
  "dimensions": "Collection_Operations#dimensions",
  "dimension": "Collection_Operations#dimension",
  "key-test": "Collection_Operations#key-test",
  "key-sequence": "Collection_Operations#key-sequence",
  "element": "Collection_Operations#element",
  "element-setter": "Collection_Operations#element-setter",
  "aref": "Collection_Operations#aref",
  "aref-setter": "Collection_Operations#aref-setter",
  "first": "Collection_Operations#first",
  "second": "Collection_Operations#second",
  "third": "Collection_Operations#third",
  "second-setter": "Collection_Operations#first-setter",
  "third-setter": "Collection_Operations#third-setter",
  "last": "Collection_Operations#last",
  "last-setter": "Collection_Operations#last-setter",
  "head": "Collection_Operations#head",
  "tail": "Collection_Operations#tail",
  "head-setter": "Collection_Operations#head-setter",
  "tail-setter": "Collection_Operations#tail-setter",
  "add": "Collection_Operations#add",
  "add!": "Collection_Operations#add.",
  "add-new": "Collection_Operations#add-new",
  "add-new!": "Collection_Operations#add-new.",
  "remove": "Collection_Operations#remove",
  "remove!": "Collection_Operations#remove.",
  "push": "Collection_Operations#push",
  "pop": "Collection_Operations#pop",
  "push-last": "Collection_Operations#push-last",
  "pop-last": "Collection_Operations#pop-last",
  "reverse": "Collection_Operations#reverse",
  "reverse!": "Collection_Operations#reverse.",
  "sort": "Collection_Operations#sort",
  "sort!": "Collection_Operations#sort.",
  "intersection": "Collection_Operations#intersection",
  "union": "Collection_Operations#union",
  "remove-duplicates": "Collection_Operations#remove-duplicates",
  "remove-duplicates!": "Collection_Operations#remove-duplicates.",
  "copy-sequence": "Collection_Operations#copy-sequence",
  "concatenate": "Collection_Operations#concatenate",
  "concatenate-as": "Collection_Operations#concatenate-as",
  "replace-subsequence!": "Collection_Operations#replace-subsequence.",
  "subsequence-position": "Collection_Operations#subsequence-position",
  "do": "Collection_Operations#do",
  "map": "Collection_Operations#map",
  "map-as": "Collection_Operations#map-as",
  "map-into": "Collection_Operations#map-into",
  "any?": "Collection_Operations#any_",
  "every?": "Collection_Operations#every_",
  "reduce": "Collection_Operations#reduce",
  "reduce1": "Collection_Operations#reduce1",
  "choose": "Collection_Operations#choose",
  "choose-by": "Collection_Operations#choose-by",
  "member?": "Collection_Operations#member_",
  "find-key": "Collection_Operations#find-key",
  "remove-key!": "Collection_Operations#remove-key.",
  "replace-elements!": "Collection_Operations#replace-elements.",
  "fill!": "Collection_Operations#fill.",
  "forward-iteration-protocol": "Collection_Operations#forward-iteration-protocol",
  "backward-iteration-protocol": "Collection_Operations#backward-iteration-protocol",
  "table-protocol": "Collection_Operations#table-protocol",
  "merge-hash-codes": "Collection_Operations#merge-hash-codes",
  "object-hash": "Collection_Operations#object-hash",
  "<condition>": "Condition_Classes#condition",
  "<serious-condition>": "Condition_Classes#serious-condition",
  "<error>": "Condition_Classes#error",
  "<simple-error>": "Condition_Classes#simple-error",
  "<type-error>": "Condition_Classes#type-error",
  "<sealed-object-error>": "Condition_Classes#sealed-object-error",
  "<warning>": "Condition_Classes#warning",
  "<simple-warning>": "Condition_Classes#simple-warning",
  "<restart>": "Condition_Classes#restart",
  "<simple-restart>": "Condition_Classes#simple-restart",
  "<abort>": "Condition_Classes#abort",
  "make": "Constructing_and_Initializing_Instances#make",
  "initialize": "Constructing_and_Initializing_Instances#initialize",
  "slot-initialized?": "Constructing_and_Initializing_Instances#slot-initialized_",
  "list": "Constructing_and_Initializing_Instances#list",
  "pair": "Constructing_and_Initializing_Instances#pair",
  "range": "Constructing_and_Initializing_Instances#range",
  "singleton": "Constructing_and_Initializing_Instances#singleton",
  "limited": "Constructing_and_Initializing_Instances#limited",
  "type-union": "Constructing_and_Initializing_Instances#type-union",
  "vector": "Constructing_and_Initializing_Instances#vector",
  "variable": "Definition_Macros#define_variable",
  "define_variable": "Definition_Macros#define_variable",
  "constant": "Definition_Macros#define_constant",
  "define_constant": "Definition_Macros#define_constant",
  "generic": "Definition_Macros#define_generic",
  "define_generic": "Definition_Macros#define_generic",
  "method": "Definition_Macros#define_method",
  "define_method": "Definition_Macros#define_method",
  "class": "Definition_Macros#define_class",
  "define_class": "Definition_Macros#define_class",
  "module": "Definition_Macros#define_module",
  "define_module": "Definition_Macros#define_module",
  "library": "Definition_Macros#define_library",
  "define_library": "Definition_Macros#define_library",
  "domain": "Definition_Macros#define_sealed_domain",
  "define_sealed_domain": "Definition_Macros#define_sealed_domain",
  "macro": "Definition_Macros#define_macro",
  "define_macro": "Definition_Macros#define_macro",
  "language:": "Dylan_Interchange_Format#language:",
  "module:": "Dylan_Interchange_Format#module:",
  "author:": "Dylan_Interchange_Format#author:",
  "==": "Equality_and_Comparison#identity",
  "~==": "Equality_and_Comparison#not_identity",
  "=": "Equality_and_Comparison#equal",
  "~=": "Equality_and_Comparison#not_equal",
  "<": "Equality_and_Comparison#less_than",
  ">": "Equality_and_Comparison#greater_than",
  "<=": "Equality_and_Comparison#less_than_or_equal",
  ">=": "Equality_and_Comparison#greater_than_or_equal",
  "min": "Equality_and_Comparison#min",
  "max": "Equality_and_Comparison#max",
  "apply": "Function_Application#apply",
  "<function>": "Function_Classes#function",
  "<generic-function>": "Function_Classes#generic-function",
  "<method>": "Function_Classes#method",
  ":=": "Function_Macros#assignment",
  "|": "Function_Macros#or",
  "&": "Function_Macros#and",
  "compose": "Functional_Operations#compose",
  "complement": "Functional_Operations#complement",
  "disjoin": "Functional_Operations#disjoin",
  "conjoin": "Functional_Operations#conjoin",
  "curry": "Functional_Operations#curry",
  "rcurry": "Functional_Operations#rcurry",
  "always": "Functional_Operations#always",
  "numbers": "Lexical_Grammar#XREF-2105",
  "let": "Local_Declaration_Macros#let",
  "local": "Local_Declaration_Macros#local",
  "handler": "Local_Declaration_Macros#let_handler",
  "let_handler": "Local_Declaration_Macros#let_handler",
  "next-method": "Method_Dispatch#HEADING-50-32",
  "<number>": "Number_Classes#number",
  "<complex>": "Number_Classes#complex",
  "<real>": "Number_Classes#real",
  "<float>": "Number_Classes#float",
  "<single-float>": "Number_Classes#single-float",
  "<double-float>": "Number_Classes#double-float",
  "<extended-float>": "Number_Classes#extended-float",
  "<rational>": "Number_Classes#rational",
  "<integer>": "Number_Classes#integer",
  "<object>": "Object_Classes#object",
  "signal": "Operations_on_Conditions#signal",
  "error": "Operations_on_Conditions#error",
  "cerror": "Operations_on_Conditions#cerror",
  "break": "Operations_on_Conditions#break",
  "check-type": "Operations_on_Conditions#check-type",
  "abort": "Operations_on_Conditions#abort",
  "default-handler": "Operations_on_Conditions#default-handler",
  "restart-query": "Operations_on_Conditions#restart-query",
  "return-query": "Operations_on_Conditions#return-query",
  "do-handlers": "Operations_on_Conditions#do-handlers",
  "return-allowed?": "Operations_on_Conditions#return-allowed_",
  "return-description": "Operations_on_Conditions#return-description",
  "condition-format-string": "Operations_on_Conditions#condition-format-string",
  "condition-format-arguments": "Operations_on_Conditions#condition-format-arguments",
  "type-error-value": "Operations_on_Conditions#type-error-value",
  "type-error-expected-type": "Operations_on_Conditions#type-error-expected-type",
  "#t": "Other_Built-In_Objects_Defined#true",
  "#f": "Other_Built-In_Objects_Defined#false",
  "$permanent-hash-state": "Other_Built-In_Objects_Defined#permanent-hash-state",
  "#()": "Other_Built-In_Objects_Defined#empty_list",
  "generic-function-methods": "Reflective_Operations_on_Functions#generic-function-methods",
  "add-method": "Reflective_Operations_on_Functions#add-method",
  "generic-function-mandatory-keywords": "Reflective_Operations_on_Functions#generic-function-mandatory-keywords",
  "function-specializers": "Reflective_Operations_on_Functions#function-specializers",
  "function-arguments": "Reflective_Operations_on_Functions#function-arguments",
  "function-return-values": "Reflective_Operations_on_Functions#function-return-values",
  "applicable-method?": "Reflective_Operations_on_Functions#applicable-method_",
  "sorted-applicable-methods": "Reflective_Operations_on_Functions#sorted-applicable-methods",
  "find-method": "Reflective_Operations_on_Functions#find-method",
  "remove-method": "Reflective_Operations_on_Functions#remove-method",
  "instance?": "Reflective_Operations_on_Types#instance_",
  "subtype?": "Reflective_Operations_on_Types#subtype_",
  "object-class": "Reflective_Operations_on_Types#object-class",
  "all-superclasses": "Reflective_Operations_on_Types#all-superclasses",
  "direct-superclasses": "Reflective_Operations_on_Types#direct-superclasses",
  "direct-subclasses": "Reflective_Operations_on_Types#direct-subclasses",
  "<character>": "Simple_Object_Classes#character",
  "<symbol>": "Simple_Object_Classes#symbol",
  "<boolean>": "Simple_Object_Classes#boolean",
  "if": "Statement_Macros#if",
  "unless": "Statement_Macros#unless",
  "case": "Statement_Macros#case",
  "select": "Statement_Macros#select",
  "while": "Statement_Macros#while",
  "until": "Statement_Macros#until",
  "for": "Statement_Macros#for",
  "begin": "Statement_Macros#begin",
  "block": "Statement_Macros#block",
  "method": "Statement_Macros#method",
  "<type>": "Type_Classes#type",
  "<class>": "Type_Classes#class",
  "<singleton>": "Type_Classes#singleton"
}

def lookup(key):
  return index.get(key.lower(), key)

