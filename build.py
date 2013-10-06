#!/usr/bin/env python
import sys, os, glob
from commandwrapper import WrapCommand

def build(filename):
    filename = os.path.basename(filename)
    basename = os.path.splitext(filename)[0]
    WrapCommand("cython --embed -I %s -o tmp/%s.c src/%s" % (get_site_package_path(), basename, filename))()
    os.chdir('tmp')
    WrapCommand("gcc -c %s.c -I%s" % (basename, get_c_include_path()))()
    WrapCommand("gcc -o ../bin/%s %s.o -l%s" % (basename, basename, get_python_name()))()
    os.chdir('..')
    empty_dir('tmp')
    print "build bin/%s" % basename

def build_all():
    files = glob.glob('src/*.py')
    for f in files:
        build(f)

def get_python_name():
    return "python%d.%d" % (sys.version_info[0], sys.version_info[1])

def get_c_include_path():
    return "%s/include/%s" % (sys.prefix, get_python_name())

def get_python_bin():
    return "%s/bin/%s" % (sys.prefix, get_python_name())

def get_site_package_path():
    return "%s/lib/%s/*/site-packages" % (sys.prefix, get_python_name())

def empty_dir(path):
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    build_all()