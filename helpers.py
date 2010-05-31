#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import inspect
import algorithms



class Singleton(type): 
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance


def logger(name=""):
    def wrapped(f):
        def _wrapped(*args, **kwargs):
            print ">>> %s.%s \n" % (name, f.func_name)
            result = f(*args, **kwargs)
            print "<<< %s.%s \n" % (name, f.func_name)
            return result
        _wrapped.__doc__ = f.__doc__
        return _wrapped
    return wrapped


def get_svn_revision(path=None):
    import os, re
    rev = None
    if path is None:
        path = os.path.dirname( __file__ )# __path__[0]
    
    entries_path = '%s/.svn/entries' % path

    if os.path.exists(entries_path):
        entries = open(entries_path, 'r').read()
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match('(\d+)', entries):
            rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    if rev:
        return u' SVN-%s' % rev
    return u'1.0'


def get_implemented():
    implemented = [alg for alg in inspect.getmembers(algorithms) if 
            inspect.isclass(alg[1]) and len(inspect.getmro(alg[1]))>1 ]
    return dict(implemented)
