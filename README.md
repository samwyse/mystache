mystache
========

An independent reimplementation of the Mustache template language in Python. Unlike Pystache, native methods are allowed on native types; i.e. in Mystache, if "{{name}}" evaluates to a native string then "{{name.upper}}" is interpolated as the same value, except in upper case. 
