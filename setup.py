from setuptools import setup, dist
from os import path, mkdir
from urllib import urlretrieve
from shutil import copy, copytree, rmtree
from distutils.dir_util import copy_tree
from glob import glob
import sys

import contextlib
import lzma
import tarfile

if sys.version_info < (3, 0, 0):
    from io import open  # python 2 builtin open doesn't have an encoding option
# from https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# default for set_library_path
cindexfile="clang/cindex.py"
with open(cindexfile, "a") as initfile:
    initfile.write(u'''
import os
import cindex
cindex.Config.set_library_path(os.path.dirname(os.path.abspath(__file__)))
''')

# get the version
package_version= open('version.txt').read()
llvm_version='.'.join(package_version.split('.')[:3])

# download clang to get python bindings
clang_src="cfe-%s.src" % llvm_version
clang_src_archive="%s.tar.xz" % clang_src
clang_src_url= "https://releases.llvm.org/%s/%s" % (llvm_version, clang_src_archive)
urlretrieve(clang_src_url, clang_src_archive)
with contextlib.closing(lzma.LZMAFile(clang_src_archive)) as xz:
    with tarfile.open(fileobj=xz) as f:
        f.extractall('.')

# deploy clang bindings
clang_bindings_root=clang_src + "/bindings/python"
clang_bindings = glob(clang_bindings_root + "/clang/*")
clang_examples = clang_bindings_root + "/examples"
clang_tests = clang_bindings_root + "/tests"
for file in clang_bindings:
    copy(file, 'clang')
copy_tree(clang_examples, 'examples')
copy_tree(clang_tests, 'tests')

setup(
    name="clang",
    author="Ethan Smith",
    author_email="ethan@ethanhs.me",
    version=package_version,
    url="https://github.com/ethanhs/clang",
    packages=["clang"],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
